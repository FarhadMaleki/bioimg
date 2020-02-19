import unittest


start_dir = './test/'
loader = unittest.TestLoader()
suite = loader.discover(start_dir)
# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
