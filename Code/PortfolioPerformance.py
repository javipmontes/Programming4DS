import pandas as pd

def return_value(go, ca , st, cb, pb, p_al, prices_paid):


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

def volatility(go, ca , st, cb, pb, p_al, prices_paid):

    p_al['shares_ST'] = p_al['ST'] * 100 / prices_paid[0]
    p_al['shares_CB'] = p_al['CB'] * 100 / prices_paid[1]
    p_al['shares_PB'] = p_al['PB'] * 100 / prices_paid[2]
    p_al['shares_GO'] = p_al['GO'] * 100 / prices_paid[3]
    p_al['shares_CA'] = p_al['CA'] * 100 / prices_paid[4]

    assets_volatility = []
    for asset in [go, ca, st, cb, pb]:
        assets_volatility.append(100 * asset.Price.std() / asset.Price.mean())

    volatility = assets_volatility[0] * p_al['shares_ST'] + assets_volatility[1] * p_al['shares_CB'] + \
                         assets_volatility[2] * p_al['shares_PB'] + assets_volatility[3] * p_al['shares_GO'] + \
                         assets_volatility[4] * p_al['shares_CA']


    return volatility

if __name__ == '__main__':

    go = pd.read_csv('data/spdr-gold-trust.csv', sep=';')
    ca = pd.read_csv('data/usdollar.csv', sep=';')
    st = pd.read_csv('data/amundi-msci-wrld-ae-c.csv', sep=';')
    cb = pd.read_csv('data/ishares-global-corporate-bond-$.csv', sep=';')
    pb = pd.read_csv('data/db-x-trackers-ii-global-sovereign-5.csv', sep=';')
    p_al = pd.read_csv('data/portfolio_allocations.csv')

    # we store the prices of the assets at the the beginning of the year
    prices_paid = []
    prices_paid.extend([st.iloc[-1]['Price'], cb.iloc[-1]['Price'], pb.iloc[-1]['Price'], go.iloc[-1]['Price'], ca.iloc[-1]['Price']])

    p_al['RETURN'] = return_value(go, ca, st, cb, pb, p_al, prices_paid)
    p_al['VOLATILITY'] = volatility(go, ca, st, cb, pb, p_al, prices_paid)
    p_al = p_al.drop(['shares_ST', 'shares_CB', 'shares_PB', 'shares_GO', 'shares_CA'], axis=1)
    p_al.to_csv('data/portfolio_metrics.csv')