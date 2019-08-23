from tkinter import Tk, Label
from math import tanh, log10
from fetch_exchanges import update_data_points
from linear_regression import gradient, square_error

window = Tk()
window.title('crypto-view')

currency_data = [
    ['BTC', 'Bitcoin'],
    ['BCH', 'Bitcoin Cash'],
    ['ETH', 'Ethereum'],
    ['ETC', 'Ethereum Classic'],
    ['LTC', 'Litecoin'],
    ['XRP', 'Ripple'],
    ['XMR', 'Monero'],
    ['REP', 'Augur'],
    ['ADA', 'Cardano'],
    ['ZEC', 'Zcash']]

for i in range(len(currency_data)):
    currency_data[i].append([])

    def label_w(j):
        label = Label(window, text='None', bg='ghost white')
        label.grid(row=i, column=j)
        return label
    currency_data[i].append([label_w(1), label_w(3), label_w(5)])

for i, (_, name, _, _) in enumerate(currency_data):
    def label(text, column): return Label(
        window, text=text).grid(row=i, column=column)

    label(f'{name} Kurs:', 0)
    label('\tAktueller Anstieg:', 2)
    label('\tFehlerwert:', 4)


def update_window():
    for i in range(len(currency_data)):
        data_points = currency_data[i][2]
        update_data_points(data_points, currency_data[i][0] + '/EUR')

        exchange = None
        if len(data_points) > 0:
            exchange = data_points[-1][1]

        grad, error = None, None
        if len(data_points) >= 2:
            grad = gradient(data_points)
            error_exp = square_error(data_points, grad=grad) / len(data_points)
            if error_exp != 0:
                error = log10(error_exp)

        labels = currency_data[i][3]

        if len(data_points) > 0:
            labels[0].config(text=str(round(exchange, 3))+' €')

        if grad != None:
            labels[1].config(
                text=str(round(grad * 1000 * 60, 4)) + ' €/min',
                fg='#%02x%02x%02x' % gradient_color(grad, exchange))

        if error != None:
            labels[2].config(text=str(round(error, 2)))

    window.after(1000, update_window)


def gradient_color(gradient, exchange=None):
    if exchange == None:
        exchange = 50

    gradient /= exchange

    red = 200, 0, 0
    green = 0, 200, 0

    tanhed = tanh(gradient * 8 * 10**7)
    dim = abs(tanhed)
    squashed = (tanhed + 1) / 2

    def component(i): return int(
        round(dim * (red[i] + squashed * (green[i] - red[i]))))
    return component(0), component(1), component(2)


window.after(1, update_window)
window.mainloop()
