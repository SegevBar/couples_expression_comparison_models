#!/bin/bash
urle () { [[ "${1}" ]] || return 1; local LANG=C i x; for (( i = 0; i < ${#1}; i++ )); do x="${1:i:1}"; [[ "${x}" == [a-zA-Z0-9.~-] ]] && echo -n "${x}" || printf '%%%02X' "'${x}"; done; echo; }

# Get project setup from configuration file
source config.cfg

current_exp_rep_generator=$EXP_REP_GENERATOR

printf "\n======== Starting Installation! ========\n\n"
echo ""

# set FLAME credentials
echo -e "Before you continue, you must register at https://flame.is.tue.mpg.de/ and agree to the FLAME license terms."
read -p "Enter your FLAME username: " username
read -p "Enter your FLAME password: " password
username=$(urle $username)
password=$(urle $password)
echo ""

# Install the configured Expression Representation Generator
case $current_exp_rep_generator in
    EMOCA)
        echo "installing EMOCA."
        cd Expression_Representation_Generators/EMOCA
        bash emoca_installation.sh
        ;;
    SPECTRE)
        echo "installing SPECTRE."
        cd Expression_Representation_Generators/SPECTRE
        bash spectre_installation.sh $username $password
        ;;
    DECA)
        echo "installing DECA."
        cd Expression_Representation_Generators/DECA
        bash deca_installation.sh $username $password
        ;;
    *)
        echo "Invalid choice! Please check the configuration file."
        ;;
esac

cd ..
echo ""
echo "Installation Finished!"