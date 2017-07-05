import tensorflow as tf
import platform
import time


py_ver = platform.python_version()
print("Tensorflow version: %s running on Python %s" % (tf.__version__, py_ver))
DEBUG = False


# a linear model is
# y = f(x) = W * x + b
# where

# W and b are variables
W = tf.Variable([.3], tf.float32)
b = tf.Variable([-.3], tf.float32)

# x is the input
x = tf.placeholder(tf.float32)
# and y is the target
y = tf.placeholder(tf.float32)

# which will be replaced by our training data
x_train = [1,2,3,4]
y_train = [0,-1,-2,-3]

# so we have the linear_model
f = W * x + b

# and the (squared error) loss function
loss = tf.reduce_sum(tf.square(f - y))

# and the (SGD) optimizer
optimizer = tf.train.GradientDescentOptimizer(0.01)

# the objective of training is to minimize the loss
train = optimizer.minimize(loss)

# we create a session and initialize the variables
init = tf.global_variables_initializer()
sess = None
if DEBUG:
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
else:
    sess = tf.Session()
sess.run(init)

print('Running.')
time_start = time.time()
# and train our model
for i in range(1000):
    sess.run(train, {x:x_train, y:y_train})

# resulting in new values for the variables
# (which should be close to W=-1 and b = 1 )
# and we can calculate the training accuracy by computing the loss on
# the training set with the new values of W and b
curr_W, curr_b, curr_loss  = sess.run([W, b, loss], {x:x_train, y:y_train})

time_elapsed = time.time() - time_start

print("W: %s b: %s loss: %s" % (curr_W, curr_b, curr_loss))
print('Finished in {}s ({}ms)'.format(int(time_elapsed),
                                      int(time_elapsed * 1000)))

