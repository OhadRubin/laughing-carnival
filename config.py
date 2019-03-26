import json
import os

class Config:
  """Configuration object loaded from/saved to JSON object
  """
  def __init__(self, config=None, path=None, params=[], clone=None):
    self.path = path
    save = True
    if clone is not None:
      self.path = clone.path
      entries = clone.__dict__	
    elif config is not None:
      entries = self._get_config(config)
      if os.path.isfile(self.path):
        print("A configuration file is already existing. It will not be overwritten")
      else:
        print("Writing configuration file: '%s'" % self.path)
        save = True

    elif path is not None:
      entries = self._load()
    else:
      raise ValueError("Parameters 'config' and 'path' can't be both 'None'")

    for param in params:
      val = params[param]
      if val is not None:
        entries[param] = val
    self.__dict__.update(entries)

    if save:
      self.save()

  def _get_config(self, config):       
    if config in ["small", "sm", "smsm", "smlg"]:
      o = small_config()
    elif config == "medium":
      o = medium_config()
    elif config in ["large", "lg", "lgsm", "lglg"]:
      o = large_config()
    else:
      raise ValueError("Invalid config: %s", config)

    if config in ["smlg", "lglg"]:
      o["vocab_size"] = 150000	
    return o

  def _load(self):
    return json.load(open(self.path))

  def save(self):
    tmp = self.path
    o = self.__dict__
    del o['path']
    json.dump(o, open(tmp, 'w'), indent=2)
    self.path = tmp

  def __str__(self):
    o = self.__dict__
    return json.dumps(o, indent=2)

def small_config():
  """Small config."""
  return {"init_scale" : 0.1,
    "learning_rate" : 1.0,
    "max_grad_norm" : 5,
    "num_layers" : 2,
    "num_steps" : 20,
    "hidden_size" : 200,
    "max_epoch" : 4,
    "max_max_epoch" : 13,
    "keep_prob" : 1.0,
    "lr_decay" : 0.5,
    "batch_size" : 20,
    "vocab_size" : 10000,
    "num_samples": 1024,
    }


def medium_config():
  """Medium config."""
  return{ 
      "init_scale" : 0.05,
      "learning_rate" : 1.0,
      "max_grad_norm" : 5,
      "num_layers" : 2,
      "num_steps" : 35,
      "hidden_size" : 650,
      "max_epoch" : 6,
      "max_max_epoch" : 39,
      "keep_prob" : 0.5,
      "lr_decay" : 0.8,
      "batch_size" : 20,
      "vocab_size" : 10000,
      "num_samples": 1024,
    }

def large_config():
  """Large config."""
  return {
      "init_scale" : 0.04,
      "learning_rate" : 1.0,
      "max_grad_norm" : 10,
      "num_layers" : 2,
      "num_steps" : 35,
      "hidden_size" : 1500,
      "max_epoch" : 14,
      "max_max_epoch" : 55,
      "keep_prob" : 0.35,
      "lr_decay" : 1 / 1.15,
      "batch_size" : 20,
      "vocab_size" : 10000,
      "num_samples": 1024,
    }
