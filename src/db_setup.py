from db_connection_manager import DbConnectionManager

class DbInitializer:
    def __init__(self):
        self.conn = DbConnectionManager().conn

        self.trunc_table('assets')
        self.trunc_table('possible_pairs')

        self.populate_assets_table()
        self.populate_possible_pairs_table()

    def assets(self):
        return [
            ['DSHBTC', 'Dash'],
            ['BATBTC', 'Basic Authentication Token'],
            ['BABBTC', 'Bitcoin Cash'],
            ['EOSBTC', 'EOS'],
            ['QTMBTC', 'Qtum'],
            ['ETCBTC', 'Etherium Classic'],
            ['ETHBTC', 'Etherium'],
            ['LTCBTC', 'Litecoin'],
            ['XLMBTC', 'Stellar Lumens'],
            ['XMRBTC', 'Monero'],
            ['ZECBTC', 'ZCash'],
            ['XTZBTC', 'Tezos'],
            ['XRPBTC', 'Ripple']
        ]

    def asset_codes(self):
        return [asset[0] for asset in self.assets()]

    def exec_query(self, query, args=None):
        cursor = self.conn.cursor()
        cursor.execute(query, args) if args else cursor.execute(query)

    def trunc_table(self, table):
        query = "TRUNCATE TABLE " + table
        self.exec_query(query)

    def populate_assets_table(self):
        for asset in self.assets():
            query = "INSERT INTO assets(code, name) VALUES(%s,%s)"
            args = (asset[0], asset[1])

            self.exec_query(query, args)

    def populate_possible_pairs_table(self):
        for asset_A in self.asset_codes():
            for asset_B in self.asset_codes():
                if not asset_A == asset_B:
                    query = "INSERT INTO possible_pairs(asset_A, asset_B) VALUES(%s,%s)"
                    args = (asset_A, asset_B)

                    self.exec_query(query, args)

if __name__ == '__main__':
    DbInitializer()
