import platform

if platform.system() == "Windows":
    import wexpect as expect_lib 
else:
    import pexpect as expect_lib
