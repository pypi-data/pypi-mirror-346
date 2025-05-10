#
#   t8setup.bash - common setup/startup for projects using t8dev
#
#   This file, which is available in the source repo only (it is not
#   distributed as part of the `t8dev` Python package) is useful for
#   setting up the environment for a t8dev build/test/run session when you
#   have t8dev source available. (Typically t8dev developers have the t8dev
#   repo as a submodule of their 8-bit development repo.)
#
#   This file should be sourced (`source` or `.`) by the top-level
#   `Test` script in projects using t8dev. Before sourcing it, the
#   T8_PROJDIR environment variable must be set with the path of
#   the project using t8dev. Further, it's helpful to initialise the
#   submodule if it's not yet been done. All this is typically done
#   with:
#
#       export T8_PROJDIR=$(cd "$(dirname "$0")" && pwd -P)
#       t8dir=tool/t8dev    # or whatever your submodule path is
#       [[ -r $T8_PROJDIR/$t8dir/t8setup.bash ]] \
#           || git submodule update --init "$T8_PROJDIR/$t8dir"
#       . "$T8_PROJDIR"/$t8dir/t8setup.bash
#
#   The setup includes:
#   • Ensures that all submodule directories of this repo have a .git/
#     directory or file and initialises any that do not.
#   • Prints a warning about any submodules that are modified from the
#     version in the head commit.
#   • Parses any known command line options at the front of $@, removing
#     them and performing their corresponding actions. (All remaining
#     command line options are left in $@.) Parsing stops at a `--`
#     option which will be left in place in case the caller needs to
#     see it to separate its own options from those to be passed to
#     e.g. pytest. (It's safe to pass the `--` straight on to pytest.)
#   • Installs the Python virtual environment and packages (if necessary)
#     and activates it.
#   • Confirms that the r8format dependency is present.
#     (XXX: should probably be done by pip.)
#   • Sets up various other paths and environment variables.
#

####################################################################
#   Confirm we are using Bash and that we're sourced, not called
#   as a subprocess. (The calling process needs the functions we
#   define and variables that we set.)

[ -n "$BASH_VERSION" ] || { echo 1>&2 "source (.) this with Bash."; exit 9; }
#   https://stackoverflow.com/a/28776166/107294
(return 0 2>/dev/null) \
    || { echo 1>&2 "source (.) $0 with Bash."; exit 9; }

####################################################################
#   Functions (used here and by the caller)

__t8_submodules_list() {
    #   Return a list of all submodule paths relative to $T8_PROJDIR.
    #   XXX This should set an array so we can handle spaces in the paths.
    local gitmodules="$T8_PROJDIR"/.gitmodules
    [[ -r $gitmodules ]] || return 0        # no file = no modules
    git config -f "$gitmodules" -l \
        | sed -n -e 's/^submodule\.//' -e 's/.*\.path=//p'
}

__t8_submodules_warn_modified() {
    #   If any submodules are modified, warn about this. Usually this is
    #   because the developer is working on submodule code (and needs to
    #   commit it before commiting her project) or the developer is testing
    #   an update to new versions of submodules.
    local sms="$(__t8_submodules_list)"
    [[ -n $sms ]] || return 0               # no modules
    git -C "$T8_PROJDIR" diff-index --quiet @ $sms || {
        echo 1>&2 '----- WARNING: submodules are modified:' \
            "$(git -C "$T8_PROJDIR" status -s $sms | tr -d '\n')"
    }
}

__t8_submodules_init_empty() {
    #   Check out any "empty" submodules in the parent project, i.e., those
    #   that appear not to be initialised because they do not have a file
    #   or directory named `.git` in their submodule directory.
    local sm
    for sm in $(__t8_submodules_list); do
        dir="$T8_PROJDIR/$sm"
        [[ -e $dir/.git ]] && continue
        echo "----- Initializing empty submodule $sm"
        (cd "$T8_PROJDIR" && git submodule update --init "$sm")
    done
}

__t8_check_r8format_dependency() {
    #   Ensure that we can import the `binary` package from r8format,
    #   as we depend on several modules from that package.
    #   XXX This should use `binary.__version__ or something like that
    #   when that becomes available.
    local pyprg='
import sys
try:
    import binary.memimage
except ModuleNotFoundError as ex:
    print("{}: {}".format(ex.__class__.__name__, ex.msg), file=sys.stderr)
    sys.exit(1)
'
    python -c "$pyprg" || {
        echo 1>&2 \
            'ERROR: r8format package not available. Install or add submodule.'
        return 8
    }
}

####################################################################
#   Main

find_t8_project_dir() {
    #   If the CWD appears to be in or under a T8 project root, we can
    #   just guess that directory as the root, and save the user the
    #   effort of explicitly defining it.
    local dir="$(pwd -P)"
    local pyvlib=.build/virtualenv/lib  # must not use glob patterns
    while [[ -n $dir ]]; do
        #   We check for an executable bin/t8dev or Scripts/t8dev.exe.
        #   This may not be the best way to do it, but should work in
        #   most circumstances.
        local xfile=$(echo "$dir"/.build/virtualenv/[bS]*/t8dev*)
        [[ -x $xfile ]] && {
            T8_PROJDIR="$dir"
            echo 1>&2 "----- WARNING: missing T8_PROJDIR set to '$dir'"
            return 0
        }
        dir=${dir%/*}
    done
    echo 1>&2 'ERROR: T8_PROJDIR not set and cannot find installed t8 project'
    return 2
}

[[ -n ${T8_PROJDIR:-} ]] || find_t8_project_dir || return $?
[[ -z ${BUILDDIR:-} ]] && BUILDDIR="$T8_PROJDIR/.build"

#   Exports are separate from setting to ensure that variables set
#   by the caller are exported by us, if the caller didn't export.
export T8_PROJDIR BUILDDIR

#   Bring in directory for tools local to this project, if not already present.
#   XXX We should probably also be bringing in the paths for discovered
#   tools external to the project, but it's not clear how to do that here,
#   since at this point the tools might not yet have been built.
[[ :$PATH: = *:$BUILDDIR/tool/bin:* ]] || PATH="$BUILDDIR/tool/bin:$PATH"

#   If the project has its own local bin/ directory, include that in
#   the path as well.
[[ -d "$T8_PROJDIR/bin" && :$PATH: != *:$T8_PROJDIR/bin:* ]] \
    && PATH="$T8_PROJDIR/bin:$PATH"

#   Leading command line args (these must be at the start):
#   • -C: clean rebuild of everything, including toolchains
#   • -c: clean rebuild of only this repo's source (test/toolchain output)
#   All args after these are left for the calling script.
while [[ ${#@} -gt 0 ]]; do case "$1" in
    --)     break;;     # NOTE: no shift here so caller can see the --
    -C)     shift; rm -rf "$BUILDDIR" ${T8_CLEAN_C-};;
    -c)     shift; rm -rf ${T8_CLEAN_c-} \
                "$BUILDDIR"/{emulator,obj,ptobj,pytest,release,virtualenv} \
                ;;
    *)      break;;
esac; done

__t8_submodules_init_empty
__t8_submodules_warn_modified
. "$(dirname "${BASH_SOURCE[0]}")"/../pactivate -B "$T8_PROJDIR" -q
__t8_check_r8format_dependency || return $?

unset \
    __t8_submodules_list __t8_submodules_warn_modified \
    __t8_submodules_init_empty __t8_submodules_pip_install_e \
    __t8_check_r8format_dependency \
    #
