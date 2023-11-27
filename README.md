# minesweeper autoplay

## Requirements
To train and run a model you need to have the following Python libraries installed
```bash
pip install pygame gymnasium time stable_baselines3
```

To visualize the training process, you need to have the following library
```bash
pip install tensorboard
```

## Train a model
To train a model, you need to run the following command (changing the path to save the model and logs)

```python
python src/model.py
```

## Run the model
In the models folder we have different time versions of the model trained with different numbers of steps (the versions were presented during the presentation and the slides can be seen in the file ```slides.pdf```). We can test a certain model using the command below, changing the global variable that points to the model

```python
python src/run_load_player.py
```

## Visualize the model
In the `logs` folder there is information obtained during model training, using the command below it can be viewed in HTML format using the ```tensorboard``` library

```bash
tensorboard --logdir=logs/logsv6 --port=6000
```