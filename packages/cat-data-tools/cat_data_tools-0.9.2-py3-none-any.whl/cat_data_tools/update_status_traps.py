def _update_status_traps(traps_info_df):
    df = traps_info_df.sort_values(by=["ID", "Fecha"])
    is_type_changed = df["Tipo"] != df["Tipo"].shift()
    is_order_changed = df["Orden"] != df["Orden"].shift()
    is_trap_status_first_apparence = ~df.duplicated(subset=["Tipo", "ID", "Orden"], keep="first")
    filtered_df = df.loc[is_type_changed | is_order_changed | is_trap_status_first_apparence]
    return filtered_df.reset_index(drop=True)
