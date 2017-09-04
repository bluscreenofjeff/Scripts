#!/bin/bash
for x in $(ls); do cd $x && git pull; cd /opt; done