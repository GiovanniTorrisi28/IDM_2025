def create_basket_sets(df, transaction_col='scontrino_id', product_col='descr_liv4', quantity_col='r_qta_pezzi'):
    # Transazioni x prodotti
    basket = (df
            .groupby([transaction_col, product_col])[quantity_col]
            .sum().unstack().reset_index().fillna(0)
            )
    # Matrice binaria di 0/1 (non presente/presente)
    basket_sets = basket.drop(transaction_col, axis=1).applymap(lambda x: 1 if x > 0 else 0)
    return basket_sets