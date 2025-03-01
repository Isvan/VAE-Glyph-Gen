# The base for most of this is from : https://www.tensorflow.org/tutorials/generative/cvae
import tensorflow as tf

class CVAE(tf.keras.Model):
  """Convolutional variational autoencoder."""

  def __init__(self, latent_dim, imgSize):
    super(CVAE, self).__init__()
    self.latent_dim = latent_dim
    self.imgSize = imgSize
    self.encoder = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=(imgSize, imgSize, 1)),
            tf.keras.layers.Conv2D(
                filters=1, kernel_size=3, strides=1, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            
            tf.keras.layers.Conv2D(
                filters=32, kernel_size=3, strides=1, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            
            tf.keras.layers.Conv2D(
                filters=64, kernel_size=3, strides=2, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            
            tf.keras.layers.Conv2D(
                filters=64, kernel_size=3, strides=1, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            
            tf.keras.layers.Flatten(),
            tf.keras.layers.LayerNormalization(),
            # No activation
            tf.keras.layers.Dense(latent_dim + latent_dim)
        ]
    )

    self.decoder = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=(latent_dim,)),
            tf.keras.layers.Dense(units=latent_dim, activation=tf.nn.relu),
            tf.keras.layers.LayerNormalization(),
            tf.keras.layers.Dense(units=16*16*32, activation=tf.nn.relu),
            tf.keras.layers.LayerNormalization(),
            tf.keras.layers.Reshape(target_shape=(16, 16, 32)),
            tf.keras.layers.Conv2DTranspose(
                filters=64, kernel_size=3, strides=1, padding='same',
                activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            
            tf.keras.layers.Conv2DTranspose(
                filters=64, kernel_size=3, strides=1, padding='same',
                activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            
            tf.keras.layers.Conv2DTranspose(
                filters=64, kernel_size=3, strides=2, padding='same',
                activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
    
            tf.keras.layers.Conv2DTranspose(
                filters=32, kernel_size=3, strides=2, padding='same',
                activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU(),
            # No activation
            tf.keras.layers.Conv2DTranspose(
                filters=1, kernel_size=3, strides=1, padding='same'),
            #tf.keras.layers.BatchNormalization(),
            #tf.keras.layers.LeakyReLU(),
        ]
    )

    #Print the Models so I can spot any issues/model mismatches
    print(self.encoder.summary())
    print(self.decoder.summary())

  @tf.function
  def sample(self, eps=None):
    if eps is None:
      eps = tf.random.normal(shape=(100, self.latent_dim))
    return self.decode(eps, apply_sigmoid=True)

  def encode(self, x):
    mean, logvar = tf.split(self.encoder(x), num_or_size_splits=2, axis=1)
    return mean, logvar

  def reparameterize(self, mean, logvar):
    eps = tf.random.normal(shape=mean.shape)
    return eps * tf.exp(logvar * .5) + mean

  def decode(self, z, apply_sigmoid=False):
    logits = self.decoder(z)
    if apply_sigmoid:
      probs = tf.sigmoid(logits)
      return probs
    return logits