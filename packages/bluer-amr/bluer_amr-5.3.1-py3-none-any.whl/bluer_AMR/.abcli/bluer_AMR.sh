#! /usr/bin/env bash

function bluer_AMR() {
    local task=$1

    bluer_ai_generic_task \
        plugin=bluer_AMR,task=$task \
        "${@:2}"
}

bluer_ai_log $(bluer_AMR version --show_icon 1)
