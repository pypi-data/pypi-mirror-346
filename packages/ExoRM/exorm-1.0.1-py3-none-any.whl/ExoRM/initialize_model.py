import matplotlib.pyplot as plot
import numpy
import os
import pandas
import pickle

from platformdirs import user_data_dir
from scipy.interpolate import UnivariateSpline

from ExoRM import ExoRM

directory = user_data_dir('ExoRM')

data = pandas.read_csv(os.path.join(directory, 'exoplanet_rm.csv'))

data = data[['radius', 'mass']].dropna().reset_index(drop = True)
data = data.sort_values('radius').reset_index(drop = True)

counts = []
result = []
for i in range(len(data['radius'])):
    while data.loc[i, 'radius'] in counts:
        data.loc[i, 'radius'] += 1e-6

    counts.append(data.loc[i, 'radius'])

data = data.sort_values('radius').reset_index(drop = True)
data = data.reset_index(drop = True)

x = data['radius']
y = data['mass']

x = numpy.log10(x)
y = numpy.log10(y)

# plot.scatter(x, y, s = 0.3)
# plot.show()

model = UnivariateSpline(x, y, k = 2, s = 335)
model = ExoRM(model, x, y)

x_smooth = numpy.linspace(-0.5, 2, 10000)
y_smooth = model(x_smooth)

min_crossing = x_smooth[numpy.argmin(numpy.abs(y_smooth - (1 / 0.279) * numpy.log10((10 ** x_smooth) / 1.008)))]
max_crossing = x_smooth[numpy.argmin(numpy.abs(y_smooth - (1 / 0.881) * numpy.log10((10 ** x_smooth) / 0.00157)))]

model.override_min(min_crossing, model(min_crossing))
model.override_max(max_crossing, model(max_crossing))

y_smooth = model(x_smooth)

# plot.scatter(x, y, s = 0.3)
# plot.plot(x_smooth, y_smooth)
# plot.show()

model.save('radius_mass_model.pkl')