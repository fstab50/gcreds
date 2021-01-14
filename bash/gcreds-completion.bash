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


function _complete_profile_subcommands(){
    local cmds="$1"
    local split='7'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_profile_subcommands -->
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


function _complete_4_horsemen_subcommands(){
    local cmds="$1"
    local split='4'       # times to split screen width
    local ct="0"
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done

    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_region_subcommands -->
}


function _refresh_subcommands(){
    ##
    ##  Valid number of parallel processes for make binary
    ##
    local cmds=$(seq 9)
    local split='4'       # times to split screen width
    local IFS=$' \t\n'
    local formatted_cmds=( $(compgen -W "${cmds}" -- "${cur}") )

    for i in "${!formatted_cmds[@]}"; do
        formatted_cmds[$i]="$(printf '%*s' "-$(($COLUMNS/$split))"  "${formatted_cmds[$i]}")"
    done
    COMPREPLY=( "${formatted_cmds[@]}")
    return 0
    #
    # <-- end function _complete_region_subcommands -->
}



function _numargs(){
    ##
    ## Returns count of number of parameter args passed
    ##
    local parameters="$1"
    local numargs=0

    if [[ ! "$parameters" ]]; then
        printf -- '%s\n' "0"
    else
        for i in $(echo $parameters); do
            numargs=$(( $numargs + 1 ))
        done
        printf -- '%s\n' "$numargs"
    fi
    return 0
    #
    # <-- end function _numargs -->
}


function _parse_compwords(){
    ##
    ##  Interogate compwords to discover which of the  5 horsemen are missing
    ##
    compwords=("${!1}")
    four=("${!2}")

    declare -a missing_words

    for key in "${four[@]}"; do
        if [[ ! "$(echo "${compwords[@]}" | grep ${key##*-})" ]]; then
            missing_words=( "${missing_words[@]}" "$key" )
        fi
    done
    printf -- '%s\n' "${missing_words[@]}"
    #
    # <-- end function _parse_compwords -->
}


function _gcreds_completions(){
    ##
    ##  Completion structures for gcreds exectuable
    ##
    local numargs numoptions cur prev initcmd

    #config_dir="$HOME/.gcreds"
    config_dir="/usr/local/lib/gcreds"
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
    accounts_compcommands='--mfa-code --profile --refresh-hours'
    mfacode_compcommands='--accounts --profile --refresh-hours'
    profile_compcommands='--accounts --mfa-code --refresh-hours'
    refresh_compcommands='--accounts --mfa-code --profile'

    #echo -e "CUR: $cur, PREV: $prev, INITCMD: $initcmd"       # debug

    case "${initcmd}" in

        '--accounts' | '--profile' | '--mfa-code' )
            ##
            ##  Return compreply with any of the 5 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--accounts' '--mfa-code'  '--profile'  '--refresh-hours' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

    esac
    case "${cur}" in

        '--ac'*)
            COMPREPLY=( $(compgen -W '--accounts' -- ${cur}) )
            return 0
            ;;

        '--aw'*)
            COMPREPLY=( $(compgen -W '--awscli' -- ${cur}) )
            return 0
            ;;

        '--c'*)
            COMPREPLY=( $(compgen -W '--clean --configure' -- ${cur}) )
            return 0
            ;;

        '--h'*)
            COMPREPLY=( $(compgen -W '--help' -- ${cur}) )
            return 0
            ;;

        '--m'*)
            COMPREPLY=( $(compgen -W '--mfa-code' -- ${cur}) )
            return 0
            ;;

        '--p'*)
            COMPREPLY=( $(compgen -W '--profile' -- ${cur}) )
            return 0
            ;;

        '--s'*)
            COMPREPLY=( $(compgen -W '--show' -- ${cur}) )
            return 0
            ;;

        '--v'*)
            COMPREPLY=( $(compgen -W '--version' -- ${cur}) )
            return 0
            ;;

    esac
    case "${prev}" in

        '--accounts')
            COMPREPLY=( $(compgen -f ${cur}) )
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

        '--refresh-hours')
            _refresh_subcommands
            return 0
            ;;

        [0-9])
            ##
            ##  Return compreply with any of the 4 comp_words that
            ##  not already present on the command line
            ##
            declare -a horsemen
            horsemen=( '--accounts' '--mfa-code'  '--profile'  '--refresh-hours' )
            subcommands=$(_parse_compwords COMP_WORDS[@] horsemen[@])
            numargs=$(_numargs "$subcommands")

            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ] && (( "$numargs" > 2 )); then
                _complete_4_horsemen_subcommands "${subcommands}"
            else
                COMPREPLY=( $(compgen -W "${subcommands}" -- ${cur}) )
            fi
            return 0
            ;;

                #_complete_refresh_compcommands "${refresh_compcommands}"

        '--awscli' | '--configure'  | 'help' | '--clean' | '--mfa-code' | '--show' | '--version')
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
