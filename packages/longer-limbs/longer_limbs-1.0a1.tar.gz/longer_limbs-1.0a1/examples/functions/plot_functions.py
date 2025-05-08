'''Plotting functions for notebooks.'''

import numpy as np
import matplotlib.pyplot as plt


def model_eval(plot_title, feature_name, predictions, labels):
    '''Plots true vs predicted values and residuals vs
    true values'''

    fig, axs = plt.subplots(1, 2, figsize=(8, 4))

    fig.suptitle(plot_title)

    axs[0].set_title('Test set predictions')
    axs[0].scatter(labels, predictions, color='black', s=0.5)
    axs[0].set_xlabel(f'true {feature_name}')
    axs[0].set_ylabel(f'predicted {feature_name}')

    axs[1].set_title('Test set residuals')
    axs[1].scatter(labels, labels - predictions, color='black', s=0.5)
    axs[1].set_xlabel(f'true {feature_name}')
    axs[1].set_ylabel(f'{feature_name} (true - predicted)')

    fig.tight_layout()


def out_of_range(sklearn_predictions, limbs_predictions, expanded_range_df):
    '''Plots calories burned vs workout time for expanded range dataset.'''

    expanded_range_df['sklearn_prediction']=sklearn_predictions
    expanded_range_df['limbs_prediction']=limbs_predictions
    in_range_df=expanded_range_df[expanded_range_df['Duration'] <= 30]
    out_range_df=expanded_range_df[expanded_range_df['Duration'] > 30]

    fig, axs = plt.subplots(1, 2, figsize=(8, 4))

    fig.suptitle('Out-of-range predictions')

    axs[0].set_title('SciKit-learn')
    axs[0].scatter(
        in_range_df['Duration'],
        in_range_df['sklearn_prediction'],
        color='black',
        s=0.5,
        label='In range'
    )
    axs[0].scatter(
        out_range_df['Duration'],
        out_range_df['sklearn_prediction'],
        color='darkred',
        s=0.5,
        label='Out of range'
    )
    axs[0].set_xlabel('Workout duration')
    axs[0].set_ylabel('Predicted calories burned')
    axs[0].set_ylim(-10, 350)
    axs[0].legend(loc='best', markerscale=7)

    axs[1].set_title('longer-limbs')
    axs[1].scatter(
        in_range_df['Duration'],
        in_range_df['limbs_prediction'],
        color='black',
        s=0.5,
        label='In range'
    )
    axs[1].scatter(
        out_range_df['Duration'],
        out_range_df['limbs_prediction'],
        color='darkred',
        s=0.5,
        label='Out of range'
    )
    axs[1].set_xlabel('Workout duration')
    axs[1].set_ylabel('Predicted calories burned')
    axs[1].set_ylim(-10, 350)
    axs[1].legend(loc='best', markerscale=7)

    fig.tight_layout()
