# https://towardsdatascience.com/using-spacy-3-0-to-build-a-custom-ner-model-c9256bea098
from exporter import jsonl_to_list
import numpy
import pandas as pd
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

# import argparse

# def generate_training_file(training_data, outdir, model = 'en_core_web_md'):
#     """ Generate a spacy training file that is used when invoking `spacy train` """
#     nlp = spacy.load(model)
#     db = DocBin() # create a DocBin object
#     for text, annot in tqdm(training_data): # data in previous format
#         doc = nlp.make_doc(text) # create doc object from text
#         ents = []
#         for start, end, label in annot["entities"]: # add character indexes
#             span = doc.char_span(start, end, label=label, alignment_mode="contract")
#             if span is None:
#                 print("Skipping entity")
#             else:
#                 ents.append(span)
#         doc.ents = ents # label the text with the ents
#         db.add(doc)
#     db.to_disk(outfile) # save the docbin object
#     print(f'Successfully wrote \'{outfile}\' to disk')

def df_to_spacy(df, outfile, model = 'en_core_web_md'):
    """ Convert a dataframe into a .spacy training file """
    nlp = spacy.load(model)
    # nlp = spacy.blank("en")
    db = DocBin() # create a DocBin object
    counter = 0
    whitespace_counter = 0
    ent_debug = []
    debug_file = open('debug_file.txt', 'w+')
    for index, row in df.iterrows():
        # Com a nova versão do Doccano, ao invés de 'data' ele exporta como 'text'.
        doc = nlp.make_doc(row['text']) # create doc object from text
        ents = []
        for start, end, label in row['label']: # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                debug_file.write(f'Start: {start} == End: {end} == Label: {label}\n')
                debug_file.write("Skipping entity\n")
                debug_file.write(f'Ents: {str(ents)}\n')
                debug_file.write('-'*10+'\n')
                counter += 1
                if ents == []:
                  whitespace_counter += 1
            else:
                debug_file.write(f'Start: {start} == End: {end} == Label: {label}\n')
                debug_file.write(f'Ents: {str(ents)}\n')
                debug_file.write(f'Span: {str(span)}\n')
                debug_file.write('-'*10+'\n')
                ents.append(span)
                # print(ents)
        doc.ents = ents # label the text with the ents
        #for ent in doc.ents:
        #  ent_debug.append(ent)
        #debug_file.write(str(doc.text))
        #for ent in enumerate(doc.ents):
        #  debug_file.write(str(ent))

        if span is not None:
          if span.start_char == 9053 and span.end_char == 9055:
            print(span.text)
            print(span.doc)

        #if span is not None:
        #  print('-'*10)
        #  print(f'Span ents: {span.ents}')
        #  print(f'Span label: {span.label_}')
        #  print(f'Span starts: {span.start_char}')
        #  print(f'Span ends: {span.end_char}')
        #else:
        #  continue

        #print(f'Doc ents: {doc.ents}')
        #print('-'*10)
        db.add(doc)
    #with open('debug_ent.txt', 'w') as debug_file:
    #  debug_file.write(str(ent_debug))
    db.to_disk(outfile) # save the docbin object
    print(f'Successfully wrote \'{outfile}\' to disk')
    print(f'Counter: {counter}')
    print(f'Whitespace counter: {whitespace_counter}')

def generate_training_file(filepath, outdir, model = 'en_core_web_md'):
    """ Convert and split a jsonl file into spacy training files that are used when invoking `spacy train` """
    df = pd.read_json(path_or_buf=filepath, lines=True)
    df = df[df['label'].str.len() > 0]                  # filter out rows without labels
    random_generator = numpy.random.default_rng().integers(low=0, high=1000000, size=1)
    print(f'Random generator value: {random_generator}')
    train=df.sample(frac=0.8,random_state=random_generator)
    test=df.drop(train.index)
    df_to_spacy(train, f'{outdir}/train.spacy', model)
    df_to_spacy(test, f'{outdir}/test.spacy', model)

if __name__ == '__main__':
    # filepath = '/spacy/datasets/admin.jsonl' # pass by arguments
    filepath = '/content/drive/MyDrive/ProjetoFinal/spacy/datasets/admin.jsonl'
    outdir = "/content/drive/MyDrive/ProjetoFinal/spacy/models"
    generate_training_file(filepath, outdir)