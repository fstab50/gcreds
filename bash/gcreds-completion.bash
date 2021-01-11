#!/usr/bin/env bash

# GPL v3 License
#
# Copyright (c) 2018 Blake Huber
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


function _complete_gcreds_commands(){
    ##
    ##  $ gcreds  <commands>
    ##
    local cmds="$1"
    local split='5'       # times to split screen width
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${COMP_WORDS[1]}") )

    for i in "${!formatted_cmds[@]}"; do
      formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
  #
  # <-- end function _complete_gcreds_commands -->
}


function _complete_accounts_compcommands(){
    ##
    ##  $ gcreds --accounts --<compcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='3'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_mfacode_compcommands -->
}


function _complete_mfacode_compcommands(){
    ##
    ##  $ gcreds --mfa-code --<compcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='3'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_mfacode_compcommands -->
}


function _complete_profile_compcommands(){
    ##
    ##  $ gcreds --mfa-code --<compcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='3'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_profile_compcommands -->
}


function _complete_refresh_compcommands(){
    ##
    ##  $ gcreds --mfa-code --<compcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='3'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_refresh_compcommands -->
}


function _complete_install_subcommands(){
    ##
    ##  $ gcreds --install <subcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='5'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_gcreds_commands -->
}


function _complete_ospackages_subcommands(){
    ##
    ##  $ gcreds --show ospackages <subcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='6'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_ospackages_subcommands -->
}


function _complete_show_subcommands(){
    ##
    ##  $ gcreds --show  <subcommands>
    ##
    local IFS=$' \t\n'
    local subcmds="$1"
    local split='5'       # times to split screen width
    declare -a formatted_cmds=( $(compgen -W "${subcmds}" -- ${cur}) )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_gcreds_commands -->
}


function _uninstall_subcommand_list(){
    ##
    ## Python version 3 major version numbers  ##
    ##

    local bin_path
    local pyversion version major

    bin_path=$(which python3 2>/dev/null)
    ref_path='/usr/local/bin'

    if [ $bin_path ]; then
        if [ "$(echo $bin_path | grep $ref_path)" ]; then
            pyversion=$(python3 --version)
            version=${pyversion#Python}
            major=${version%.*}
        fi
    else
        major=""
    fi
    printf -- '%s\n' "$major"
}


function _gcreds_completions(){
    ##
    ##  Completion structures for gcreds exectuable
    ##
    local numargs numoptions cur prev initcmd

    config_dir="$HOME/.gcreds"
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    initcmd="${COMP_WORDS[COMP_CWORD-2]}"
    #echo "cur: $cur, prev: $prev"

    # initialize vars
    COMPREPLY=()
    numargs=0
    numoptions=0

    # option strings
    commands='--accounts --awscli --configure --clean --help --mfa-code --profile --mfa-code --show --version'

    # complementary command sets
    accounts_compcommands='--mfa-code --profile --refresh'
    mfacode_compcommands='--accounts --profile --refresh'
    profile_compcommands='--accounts --mfa-code --refresh'
    refresh_compcommands='--accounts --mfa-code --profile'

    #echo -e "CUR: $cur, PREV: $prev, INITCMD: $initcmd"       # debug

    case "${initcmd}" in
        '--accounts')
            if [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ]; then
                COMPREPLY=( $(compgen -W "--refresh --profile" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code --profile" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code --refresh" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--refresh" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--profile" -- ${cur}) )
                return 0

            else
                _complete_accounts_compcommands "${accounts_compcommands}"
            fi
            return 0
            ;;

        '--profile')
            if [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code --refresh" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ]; then
                COMPREPLY=( $(compgen -W "--accounts --refresh" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--accounts --mfa-code" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--accounts" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ]; then
                COMPREPLY=( $(compgen -W "--refresh" -- ${cur}) )
                return 0

            else
                _complete_profile_compcommands "${profile_compcommands}"
            fi
            return 0
            ;;
    esac
    case "${cur}" in
        '--awscli' | '--configure'  | 'help' | '--purge' | '--show' | '--version')
            return 0
            ;;
    esac
    case "${prev}" in

        '--accounts')
            echo $(ls .)
            ;;

        '--mfa-code')
            if [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ]; then
                COMPREPLY=( $(compgen -W "--refresh --profile" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--accounts --profile" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--accounts --refresh" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--refresh" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--accounts" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-refresh')" ]; then
                COMPREPLY=( $(compgen -W "--profile" -- ${cur}) )
                return 0

            else
                _complete_mfacode_compcommands "${mfacode_compcommands}"
            fi
            return 0
            ;;

        '--profile')
            python3=$(which python3)
            iam_users=$($python3 "$config_dir/iam_users.py")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then

                # display full completion subcommands
                _complete_profile_subcommands "${iam_users}"

            else
                COMPREPLY=( $(compgen -W "${iam_users}" -- ${cur}) )
            fi
            return 0
            ;;

        '--refresh')
            if [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
               [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code --profile" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ]; then
                COMPREPLY=( $(compgen -W "--accounts --profile" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--accounts --mfa-code" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--mfa-code" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-profile')" ]; then
                COMPREPLY=( $(compgen -W "--accounts" -- ${cur}) )
                return 0

            elif [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-accounts')" ] && \
                 [ "$(echo "${COMP_WORDS[@]}" | grep '\-\-mfa-code')" ]; then
                COMPREPLY=( $(compgen -W "--profile" -- ${cur}) )
                return 0

            else
                _complete_refresh_compcommands "${refresh_compcommands}"
            fi
            return 0
            ;;

        '--awscli' | '--configure'  | 'help' | '--purge' | '--show' | '--version')
            return 0
            ;;

        'gcreds')
            if [ "$cur" = "" ] || [ "$cur" = "--" ]; then

                _complete_gcreds_commands "${commands}"
                return 0

            fi
            ;;
    esac

    COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )

} && complete -F _gcreds_completions gcreds
