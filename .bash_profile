
alias Flatiron='ssh -p 61022 storto@gateway.flatironinstitute.org'
alias Mountceph='sshfs storto@gateway.flatironinstitute.org:/mnt/ceph/users/storto /Users/sammextee/ceph -o volname=ceph -p 61022'
alias Mounthome='sshfs storto@gateway.flatironinstitute.org:/mnt/home/storto /Users/sammextee/home -o volname=home -p 61022'


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/opt/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/opt/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

