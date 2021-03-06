import hypertune
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import argparse


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--learning_rate',
      required=True,
      type=float,
      help='learning rate')
  parser.add_argument(
      '--iterations',
      required=True,
      type=int,
      help='iterations')
  parser.add_argument(
      '--dataset_train_path',
      required=True,
      type=str
  )
  parser.add_argument(
      '--dataset_validation_path',
      required=True,
      type=str
  )


  args = parser.parse_args()
    
  return args

def model(learning_rate,iterations,dataset_train_path,dataset_validation_path):
    
  df_train = pd.read_csv(dataset_train_path)
  df_validation = pd.read_csv(dataset_validation_path)

  pipeline = Pipeline([('classifier', SGDClassifier(loss='log'))])

  X_train = df_train.drop('classEncoder', axis=1)
  y_train = df_train['classEncoder']

  pipeline.set_params(classifier__alpha=learning_rate, classifier__max_iter=iterations)
  pipeline.fit(X_train, y_train)


  X_validation = df_validation.drop('classEncoder', axis=1)
  y_validation = df_validation['classEncoder']
  accuracy = pipeline.score(X_validation, y_validation)

  hpt = hypertune.HyperTune()
  hpt.report_hyperparameter_tuning_metric(
        hyperparameter_metric_tag='accuracy', metric_value=accuracy)

def main():
  args = get_args()
  model(learning_rate=args.learning_rate,iterations=args.iterations,
                dataset_train_path=args.dataset_train_path,dataset_validation_path=args.dataset_validation_path )
    
if __name__ == "__main__":
    main()