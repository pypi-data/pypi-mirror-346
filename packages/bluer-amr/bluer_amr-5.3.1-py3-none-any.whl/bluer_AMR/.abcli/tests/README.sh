#! /usr/bin/env bash

function test_bluer_AMR_README() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_AMR build_README
}
