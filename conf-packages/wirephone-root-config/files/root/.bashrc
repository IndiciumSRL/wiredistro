#
# /etc/profile: system-wide defaults for bash(1) login shells
#
if [ ! -f ~/.inputrc ]; then
    export INPUTRC="/etc/inputrc"
fi

export LESSCHARSET="latin1"
export LESS="-R"
export CHARSET="ISO-8859-1"
export PS1='\n\[\033[01;31m\]\u@\h\[\033[01;36m\] [\d \@] \[\033[01;33m\] \w\n\[\033[00m\]<\#>:'
export PS2="\[\033[1m\]> \[\033[0m\]"
export VISUAL=vim
export GIT_SSL_NO_VERIFY=true

umask 022
alias jgit='git commit --author "Joao Mesquita <jmesquita@indicium.com.ar>"'
alias fgit='git commit --author "Federico Castro <fcastro@indicium.com.ar>"'
alias fsgdb='gdb /usr/bin/freeswitch `cat /var/run/freeswitch/freeswitch.pid`'
alias fscore='gdb /usr/bin/freeswitch `ls -rt core.* | tail -n1`'
# End of file
