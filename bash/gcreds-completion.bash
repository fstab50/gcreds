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


function _all_parameters(){
    ##
    ##    validates all subcommands provided or not
    ##
    declare -a check_words=("${!1}")
    declare -a commandline="${COMP_WORDS[*]}"

    for word in "${commandline[@]}"; do
        if [[ ! $(echo "${check_words[@]}" | grep $word) ]]; then
            return 1
        fi
    done
    return 0
}


function _current_downloads(){
    ##
    ##  Examines local fs for downloaded artifacts
    ##
    ##      - returns entry for each python binary set downloaded to /tmp
    ##
    local index="0"
    declare -a arr_targets xz tgz

    xz=( $(find /tmp -name \*.tar.xz 2>/dev/null) )
    tgz=( $(find /tmp -name \*.tgz 2>/dev/null) )

    for i in "${xz[@]}"; do
        temp="$(echo $i | awk -F '.tar' '{print $1}' | awk -F '.' '{print $1"."$2}')"
        xz[$index]=$(echo $temp | awk -F '/' '{print $NF}')
        (( index++ ))
    done

    index="0"

    for i in "${tgz[@]}"; do
        temp="$(echo $i | awk -F '.tgz' '{print $1}' | awk -F '.' '{print $1"."$2}')"
        tgz[$index]=$(echo $temp | awk -F '/' '{print $NF}')
        (( index++ ))
    done

    arr_targets=( $(echo "${xz[@]}") $(echo "${tgz[@]}") )
    echo "${arr_targets[@]}"
    #
    # <--- end function _clean_subcommands --->
}


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


function _complete_download_subcommands(){
    ##
    ##  $ gcreds --download <subcommands>
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

    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    initcmd="${COMP_WORDS[COMP_CWORD-2]}"
    #echo "cur: $cur, prev: $prev"

    # initialize vars
    COMPREPLY=()
    numargs=0
    numoptions=0

    # option strings
    commands='--accounts --awscli --configure --clean --help --mfa-code --profile --refresh --show --version'

    # install parameters
    install_commands='--install --optimizations --quiet'
    install_options='--optimizations --parallel-processes --quiet'

    # subcommand sets
    download_subcommands=$(echo "${arr_all[@]}")
    show_subcommands="$(echo "${arr_all[@]}") os-packages downloads"
    install_subcommands="$(_version3_subcommand_list) Python-2.6 Python-2.7 os-packages help"


    #echo -e "CUR: $cur, PREV: $prev, INITCMD: $initcmd"       # debug

    case "${initcmd}" in
        '--uninstall')
            case "${prev}" in
                'Python-'[0-9].[0-9] | [0-9].[0-9])
                    COMPREPLY=( $(compgen -W "${uninstall_options}" -- ${cur}) )
                    return 0
                    ;;
            esac
            ;;

    esac
    case "${cur}" in
        '--awscli' | '--configure'  | 'help' | '--purge' | '--show' | '--version')
            return 0
            ;;

        '1-None' | '2' | '3' | '4-Default' | '5' | '6' | '7' | '8' | '9')
            # parallel-processes subcmds: this section is never executed for some reason
            if [[ $(echo "${COMP_WORDS[@]}" | grep '\-\-quiet') ]] && \
               [[ $(echo "${COMP_WORDS[@]}" | grep '\-\-optimizations') ]]; then
                return 0

            elif [[ $(echo "${COMP_WORDS[@]}" | grep '\-\-quiet') ]]; then
                COMPREPLY=( $(compgen -W "--optimizations" -- ${cur}) )

            elif [[ $(echo "${COMP_WORDS[@]}" | grep '\-\-optimizations') ]]; then
                COMPREPLY=( $(compgen -W "--quiet" -- ${cur}) )

            else
                COMPREPLY=( $(compgen -W "--quiet --optimizations" -- ${cur}) )
            fi
            return 0
            ;;
    esac
    case "${prev}" in

        '--accounts')
            if [[ $(echo "${COMP_WORDS[@]}" | grep '\-\-uninstall') ]]; then
                return 0
            else
                # assemble subcommands
                clean_subcommands="$(_current_downloads) ALL"
                # return reply
                COMPREPLY=( $(compgen -W "${clean_subcommands}" -- ${cur}) )
                return 0
            fi
            ;;

        '--awscli')
            _complete_download_subcommands "${download_subcommands}"
            return 0
            ;;

        '--configure')
            if [ "$cur" = "" ] || [ "$cur" = "--" ]; then
                _complete_install_subcommands "${install_subcommands}"
            else
                COMPREPLY=( $(compgen -W "${install_subcommands}" -- ${cur}) )
            fi
            return 0
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
            fi
            return 0
            ;;

        '--profile')
            if [[ $(echo "${COMP_WORDS[@]}" | grep '\-\-uninstall') ]]; then
                return 0
            else
                COMPREPLY=( $(compgen -W "${uninstall_commands}" -- ${cur}) )
                return 0
            fi
            ;;

        '--refresh')
            # assemble subcommands
            uninstall_subcommands=$(_uninstall_subcommand_list)
            # return reply
            COMPREPLY=( $(compgen -W "${uninstall_subcommands}" -- ${cur}) )
            return 0
            ;;

        '--show')
            # assemble subcommands
            uninstall_subcommands=$(_uninstall_subcommand_list)
            # return reply
            COMPREPLY=( $(compgen -W "${uninstall_subcommands}" -- ${cur}) )
            return 0
            ;;

        '--awscli' | '--configure'  | 'help' | '--purge' | '--show' | '--version')
            return 0
            ;;

        'os-packages')
            return 0
            #  --- option code below not yet ga --- #
            if [ "$cur" = "" ] || [ "$cur" = "-" ] || [ "$cur" = "--" ]; then
                _complete_ospackages_subcommands  "${os_distributions}"
            else
                COMPREPLY=( $(compgen -W "${os_distributions}" -- ${cur}) )
            fi
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
