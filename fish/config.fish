set fish_greetin ""

alias grep='grep --color=auto'
alias cat "bat --style=plain --paging=never"
alias cat='ccat -G Plaintext="blink" -G Keyword="green" -G String="darkgreen" -G Punctuation="red" -G Comment="faint"'
alias ls='exa --group-directories-first'
alias tree='exa -T'

if status is-interactive
    # Commands to run in interactive sessions can go here
end
