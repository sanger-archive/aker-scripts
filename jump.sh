#!/bin/bash

env=$1
app=$2

case "$env" in
    wip)   jumphost='wip.aker.sanger.ac.uk' ;;
    uat)   jumphost='uat.aker.sanger.ac.uk' ;;
    prod*) jumphost='aker.sanger.ac.uk' ;;
    disp)  jumphost='disp.aker.sanger.ac.uk' ;;
    '')    echo "Usage: jump (wip|uat|prod|disp) (target)"
           exit 1
           ;;
    *)     echo "Invalid jump host:" $env
           exit 1
           ;;
esac

case "$app" in
    dash*)      target='192.168.0.21' ;;
    auth*)      target='192.168.0.21' ;;
    rec*)       target='192.168.0.22' ;;
    work*)      target='192.168.0.23' ;;
    perm*app*)  target='192.168.0.24' ;;
    proj*)      target='192.168.0.25' ;;
    setsh*)     target='192.168.0.26' ;;
    set-sh*)    target='192.168.0.26' ;;
    shape*)     target='192.168.0.26' ;;
    mat*)       target='192.168.0.27' ;;
    perm*ser*)  target='192.168.0.28' ;;
    set*)       target='192.168.0.29' ;;

    inbox)      target='192.168.0.30' ;;
    notif*)     target='192.168.0.30' ;;
    hmdmc*)     target='192.168.0.30' ;;
    bill*)      target='192.168.0.30' ;;
    ubw*)       target='192.168.0.30' ;;
    
    seq*)       target='192.168.0.34' ;;

    perm*)      echo "For permission specify 'perm-ser' or 'perm-app'"
                exit 1
                ;;

    '')         echo "Usage: jump (wip|uat|prod|disp) (target)"
                exit 1
                ;;
    *)          echo "Invalid target:" $app
                exit 1
                ;;
esac

ssh -J $jumphost $target
