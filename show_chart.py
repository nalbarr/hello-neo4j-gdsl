import altair as alt

from vega_datasets import data
cars = data.cars()

print("type(cars): ", type(cars))

print("cars.head", cars.head)


chart = alt.Chart(cars).mark_point().encode(
        x='Horsepower',
        y='Horsepower',
        color='Origin',
).interactive()

chart.show()
