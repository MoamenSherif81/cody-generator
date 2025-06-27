from Model.sampleFromImage import load_model_and_sampler

trained_weights_path = "plus/ModelParameters/bin_all_terms_depth4_10000/Extra/bin"
trained_model_name = "pix2code_model"
model, sampler = load_model_and_sampler(trained_weights_path, trained_model_name)
