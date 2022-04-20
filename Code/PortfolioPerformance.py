import pandas as pd

def return_value():
    go = pd.read_csv('data/spdr-gold-trust.csv')
    ca = pd.read_csv('data/usdollar.csv')
    st = pd.read_csv('data/amundi-msci-wrld-ae-c.csv')
    cb = pd.read_csv('data/ishares-global-corporate-bond-$.csv')
    pb = pd.read_csv('data/db-x-trackers-ii-global-sovereign-5.csv')
    p_al = pd.read_csv('data/portfolio_allocations.csv')

    #we store the prices of the assets at the the beginning of the year
    prices_paid = []
    prices_paid.extend([st.iloc[-1]['Price'], cb.iloc[-1]['Price'], pb.iloc[-1]['Price'], go.iloc[-1]['Price'], ca.iloc[-1]['Price']])

    #we calculate the buy amount with the prices of the assets at the beginning of the year
    buy_amount = []
    for i in range(len(p_al)):
        buy_amount.append(p_al.iloc[i]['ST'] * prices_paid[0] + p_al.iloc[i]['CB'] * prices_paid[1] +
                          p_al.iloc[i]['PB'] * prices_paid[2] + p_al.iloc[i]['GO'] * prices_paid[3] +
                          p_al.iloc[i]['CA'] * prices_paid[4])

    # we store the prices of the assets at the the end of the year
    prices_currently = []
    prices_currently.extend([st.iloc[0]['Price'], cb.iloc[0]['Price'], pb.iloc[0]['Price'], go.iloc[0]['Price'], ca.iloc[0]['Price']])

    # we calculate the current value with the prices of the assets at the end of the year
    current_value = []
    for i in range(len(p_al)):
        current_value.append(p_al.iloc[i]['ST'] * prices_currently[0] + p_al.iloc[i]['CB'] * prices_currently[1] +
                             p_al.iloc[i]['PB'] * prices_currently[2] + p_al.iloc[i]['GO'] * prices_currently[3] +
                             p_al.iloc[i]['CA'] * prices_currently[4])

    #we find the return value by applying the formule to all the portfolio allocations
    portfolio_return = []
    for i in range(len(p_al)):
        portfolio_return.append((current_value[i] - buy_amount[i]) / buy_amount[i] * 100)

    return portfolio_return

    def volatility():


if __name__ == '__main__':

    portfolio_return = return_value()
    p_al = pd.read_csv('data/portfolio_allocations.csv')
    p_al['RETURN'] = portfolio_return