from country_state_city import Country, State, City

countries = Country.get_countries()
country_names = {c.name: c for c in countries}
states = State.get_states_of_country(country_names['India'].iso2)
print(states)
