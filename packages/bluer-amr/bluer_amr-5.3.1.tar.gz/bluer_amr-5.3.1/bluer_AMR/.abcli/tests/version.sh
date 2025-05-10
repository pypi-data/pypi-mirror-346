#! /usr/bin/env bash

function test_bluer_AMR_version() {
    local options=$1

    bluer_ai_eval ,$options \
        "bluer_AMR version ${@:2}"
}
