from chemcrow import ChemCrow

chem_model = ChemCrow(model="gpt-4-0613", temp=0.1, verbose=True)
chem_model.run("What is the melting point of water?")