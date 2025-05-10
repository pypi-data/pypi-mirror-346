#! /usr/bin/env bash

function test_bluer_AMR_help() {
    local options=$1

    local module
    for module in \
        "@AMR" \
        \
        "@AMR pypi" \
        "@AMR pypi browse" \
        "@AMR pypi build" \
        "@AMR pypi install" \
        \
        "@AMR pytest" \
        \
        "@AMR test" \
        "@AMR test list" \
        \
        "bluer_AMR"; do
        bluer_ai_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done

    return 0
}
