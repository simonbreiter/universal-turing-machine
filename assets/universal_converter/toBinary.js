function convertToBinary(config, inputForOwnMachine) {
  // result
  var result = '';
  // prepare for problem with q0
  var addOne = false;
  if (config['q0']) {
    addOne = true;
  }

  //define conversions
  var convertTable = {
    "0": "0",
    "1": "00",
    " ": "000",
    "left": "0",
    "right": "00"
  };

  for (var stateName in config) {
    if (config.hasOwnProperty(stateName)) {
      var state = config[stateName];
      var binaryStateName = getBinaryStateName(stateName);

      for (var transitionName in state) {
        if (state.hasOwnProperty(transitionName)) {
          var transition = state[transitionName];
          if (transition.nextState === 'qdone') {
            break;
          }
          var binaryTransition = '';
          binaryTransition += binaryStateName;
          binaryTransition += '1';
          binaryTransition += convertTable[transitionName];
          binaryTransition += '1';
          binaryTransition += getBinaryStateName(transition.nextState);
          binaryTransition += '1';
          binaryTransition += convertTable[transition.write];
          binaryTransition += '1';
          binaryTransition += convertTable[transition.move];

          result += binaryTransition;
          result += '11';
        }
      }
    }
  }
  result += '1';
  if (inputForOwnMachine) {
    result += inputForOwnMachine;
  }
  return result;

  function getBinaryStateName(stateName) {
    var stateNumber = parseInt(stateName.replace('q', ''));
    var binaryStateName = addOne ? '0' : '';
    for (var i = 0; i < stateNumber; i++) {
      binaryStateName += '0';
    }
    return binaryStateName;
  }

}

