from morepath.framehack import caller_package
def my_experiment():
    return caller_package()
print '*********************'
print my_experiment()
print '*********************'
