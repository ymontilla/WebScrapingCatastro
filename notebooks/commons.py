import argparse

# +
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

# +
INPUT_PATH = "/data/posts/2020-09-26/raw"
OUTPUT_PATH = "/data/posts/2020-09-26/clean"

TEMPLATE_PATH = "/{property_type}/{city}-{post_type}/posts.parquet"
# -

coordinates_bounds = {
    'manizales': {
        'lat': {
            'lower': 5.017395,
            'upper': 5.119305
        },
        'lon':{
            'lower': -75.556431,
            'upper': -75.410519
        }
    },
    'fusagasuga': {
        'lat': {
            'lower': 5.017395,
            'upper': 5.119305
        },
        'lon':{
            'lower': -75.556431,
            'upper': -75.410519
        }
    },
    'villavicencio': {
        'lat': {
            'lower': 5.017395,
            'upper': 5.119305
        },
        'lon':{
            'lower': -75.556431,
            'upper': -75.410519
        }
    }
}


def get_args(args):
    ## Validad la ciudad
    if not args.city:
        raise Exception('ERROR', 'Se debe proveer un nombre de ciudad')
    
    city = args.city
    
    if not city in ["manizales", "fusagasuga", "villavicencio"]:
        raise Exception('ERROR', 'La ciudad debe ser una de estas 3: manizales, fusagasuga, villavicencio')
    
    ## Valida el tipo de propiedad
    if not args.property_type:
        raise Exception('ERROR', 'Se debe proveer un tipo de inmueble')
    
    property_type = args.property_type
    
    if not property_type in ["apartamentos", "casas"]:
        raise Exception('ERROR', 'Solo se soportan publicaciones de casas y apartamentos')
        
    ## Valida el tipo de la publicacion
    if not args.post_type:
        raise Exception('ERROR', 'Se debe proveer un tipo de publicacion')
    
    post_type = args.post_type
    
    if not post_type in ["arriendo", "venta"]:
        raise Exception('ERROR', 'Solo se soportan publicaciones de arriendo y venta')
    
    return city, property_type, post_type


# +
def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", help="nombre de la ciudad",
                        required=False)
    parser.add_argument("--property_type", help="nombre de la ciudad",
                    required=False)
    parser.add_argument("--post_type", help="nombre de la ciudad",
                required=False)
    
    args, unknown = parser.parse_known_args()
    
    return get_args()

def gen_paths(city, property_type, post_type):
    ## Creates input/output variables
    template_path = TEMPLATE_PATH.format(
        property_type=property_type, city=city, post_type=post_type
    )
    
    input_path = INPUT_PATH + template_path
    output_path = OUTPUT_PATH + template_path
    
    return input_path, output_path
# -



SOURCE_PATH = "/data/{source}/2020-10-16/puntos_interes_{city}.parquet"


def get_args_variables(args):
    ## Valida la fuente de datos
    if not args.source:
        raise Exception('ERROR', 'Se debe proveer una fuente de datos')
    
    source = args.source
    
    ## Valida el tipo de propiedad
    if not args.city:
        raise Exception('ERROR', 'Se debe proveer un nombre de ciudad')
    
    city = args.city
    
    if not city in ["PLACES", "OSM"]:
        raise Exception('ERROR', 'Solo se soportan las fuentes OSM y PLACES')

    return source


# +
def check_args_variables():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="nombre de la ciudad",
                        required=False)
    parser.add_argument("--city", help="nombre de la ciudad",
                        required=False)
    
    args, unknown = parser.parse_known_args()
    
    return get_args_variables()

def gen_paths_variables(source, city):
    ## Creates input/output variables
    source_path = SOURCE_PATH.format(
        source=source, city=city
    )
    
    return source_path
# -



# +
## https://www.kaggle.com/willkoehrsen/introduction-to-feature-selection

import matplotlib.pyplot as plt

def plot_feature_importances(df, threshold = 0.9):
    """
    Plots 15 most important features and the cumulative importance of features.
    Prints the number of features needed to reach threshold cumulative importance.
    
    Parameters
    --------
    df : dataframe
        Dataframe of feature importances. Columns must be feature and importance
    threshold : float, default = 0.9
        Threshold for prining information about cumulative importances
        
    Return
    --------
    df : dataframe
        Dataframe ordered by feature importances with a normalized column (sums to 1)
        and a cumulative importance column
    
    """
    
    plt.rcParams['font.size'] = 18
    
    # Sort features according to importance
    df = df.sort_values('importance', ascending = False).reset_index()
    
    # Normalize the feature importances to add up to one
    df['importance_normalized'] = df['importance'] / df['importance'].sum()
    df['cumulative_importance'] = np.cumsum(df['importance_normalized'])

    # Make a horizontal bar chart of feature importances
    plt.figure(figsize = (10, 6))
    ax = plt.subplot()
    
    # Need to reverse the index to plot most important on top
    ax.barh(list(reversed(list(df.index[:15]))), 
            df['importance_normalized'].head(15), 
            align = 'center', edgecolor = 'k')
    
    # Set the yticks and labels
    ax.set_yticks(list(reversed(list(df.index[:15]))))
    ax.set_yticklabels(df['feature'].head(15))
    
    # Plot labeling
    plt.xlabel('Normalized Importance'); plt.title('Feature Importances')
    plt.show()
    
    # Cumulative importance plot
    plt.figure(figsize = (8, 6))
    plt.plot(list(range(len(df))), df['cumulative_importance'], 'r-')
    plt.xlabel('Number of Features'); plt.ylabel('Cumulative Importance'); 
    plt.title('Cumulative Feature Importance');
    plt.show();
    
    importance_index = np.min(np.where(df['cumulative_importance'] > threshold))
    print('%d features required for %0.2f of cumulative importance' % (importance_index + 1, threshold))
    
    return df
