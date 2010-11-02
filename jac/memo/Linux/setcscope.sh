find ./* -name '*.[chsS]' > cscope.files
cscope -bkq
ctags -R