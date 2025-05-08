from flask import Blueprint, render_template, request, session, send_from_directory, current_app, jsonify
import os, tempfile, subprocess, json, glob
from PyQt5 import QtCore
import numpy as np
# Conditionally import swag_from or create a dummy decorator
try:
    from flasgger import swag_from
    print("INFO: flasgger found, API documentation enabled.")
except ImportError:
    print("WARNING: flasgger not found. API documentation will be disabled.")
    # Define a dummy decorator that does nothing
    def dummy_swag_from(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    # Assign the dummy decorator to the swag_from name
    swag_from = dummy_swag_from

bly = Blueprint('blockly', __name__)

showStatusSignal = None
kpyPath = 'kpy'
blockly_ip = ''
blocklyPath = ''

trigger=True


@bly.route('/')
def homeindex():
	return render_template('index.html')


p = None
def setBlocklyPath(pth, ip):
    global blocklyPath, local_ip
    blocklyPath = pth
    print('blockly at',pth)
    blockly_ip = ip

def setShowStatusSignal(sig):
    global showStatusSignal
    showStatusSignal = sig

def setP(dev):
    global p
    p = dev

@bly.route('/visual')
def index():
    return render_template('visual.html')


@bly.route('/editor')
def javaeditor():
    return render_template('editor.html')


@bly.route('/apps/<template_name>')
def render_template_dynamic(template_name):
    # Check if the template exists
    try:
        # Try to render the template with the given name
        template_path = f"{template_name}.html"
        return render_template(template_path)
    except Exception as e:
        # If template doesn't exist or there's an error, return 404
        return jsonify({'status': 'error', 'message': f'Template not found or error: {str(e)}'}), 404



@bly.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'logo.png', mimetype='image/png')

@bly.route('/loadxml', methods=['GET'])
def load_xml():
    file = request.args.get('file')
    # Do something with the file (e.g., load it, process it, etc.)
    # For now, return a dummy response
    print(file, blocklyPath)
    f =  open(os.path.join(blocklyPath,'samples',file+'.xml')).read()
    return jsonify({'status': 'success', 'message': f'Loaded {file}','xml':f})

@bly.route('/loadpng', methods=['GET'])
def load_thumbnail():
    file = request.args.get('file')
    print(f"Looking for thumbnail for {file}")
    
    # Check for various image formats
    image_extensions = ['.png', '.jpg', '.jpeg']
    
    for ext in image_extensions:
        thumbnail_path = os.path.join(blocklyPath, 'samples', file + ext)
        if os.path.exists(thumbnail_path):
            print(f"Found thumbnail: {thumbnail_path}")
            # Return the file with appropriate mimetype
            mimetype = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
            return send_from_directory(os.path.join(blocklyPath, 'samples'), file + ext, mimetype=mimetype)
    
    # If no image found, return a 404
    return jsonify({'status': 'error', 'message': 'No thumbnail found'}), 404

@bly.route('/get_device_status', methods=['GET'])
@swag_from('swagger_docs/get_device_status.yml')
def get_device_status():
    if p is not None:
        return jsonify({'connected': p.connected})
    else:
        return jsonify({'connected': False})



@bly.route('/set_pv1/<float:value>', methods=['GET'])
@swag_from({
    'tags': ['Power Supply'],
    'summary': 'Set the voltage for Voltage source 1 (-5 to 5 Volts) PV1',
    'parameters': [
        {
            'name': 'value',
            'in': 'path',
            'required': True,
            'description': 'The desired voltage value.',
            'schema': {'type': 'number', 'format': 'float'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Voltage set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': { # Assuming error if device not connected maps to 500
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
        }
    }
})
def set_pv1(value):
    if p is not None:
        actual_voltage = p.set_pv1(value)  # Set voltage on PV1
        return jsonify({'status': 'success', 'message': f'Set voltage on PV1 to {actual_voltage}V'})
    return jsonify({'status': 'error', 'message': 'Device not connected'}), 500

@bly.route('/set_pv2/<float:value>', methods=['GET'])
@swag_from({
    'tags': ['Power Supply'],
    'summary': 'Set the voltage for Power Voltage source 2 (PV2).',
    'parameters': [
        {
            'name': 'value',
            'in': 'path',
            'required': True,
            'description': 'The desired voltage value.',
            'schema': {'type': 'number', 'format': 'float'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Voltage set successfully.',
             'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
       },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
        }
    }
})
def set_pv2(value):
    if p is not None:
        actual_voltage = p.set_pv2(value)  # Set voltage on PV2
        return jsonify({'status': 'success', 'message': f'Set voltage on PV2 to {actual_voltage}V'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_voltage/<string:channel>', methods=['GET'])
@swag_from({
    'tags': ['Measurement'],
    'summary': 'Measure voltage from a specified analog input channel.',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The name of the channel (e.g., "A1", "A2").',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Voltage measurement successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'channel': {'type': 'string'},
                            'voltage': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
             'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
       }
    }
})
def get_voltage(channel):
    if p is not None:
        voltage = p.get_voltage(channel)  # Measure voltage from specified channel
        return jsonify({'status': 'success', 'channel': channel, 'voltage': voltage})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_voltage_time/<string:channel>', methods=['GET'])
@swag_from({
    'tags': ['Measurement'],
    'summary': 'Measure voltage with timestamp from a specified channel.',
    'operationId': 'getVoltageTime',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The name of the channel (e.g., "A1", "A2").',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Voltage measurement with timestamp successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'channel': {'type': 'string'},
                            'timestamp': {'type': 'number', 'format': 'float'},
                            'voltage': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
        }
    }
})
def get_voltage_time(channel):
    if p is not None:
        t, v = p.get_voltage_time()  # Measure voltage with timestamp
        return jsonify({'status': 'success', 'channel': channel, 'timestamp': t, 'voltage': v})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_average_voltage', methods=['GET'])
@swag_from({
    'tags': ['Measurement'],
    'summary': 'Get average voltage over multiple samples.',
    'operationId': 'getAverageVoltage',
    'description': 'Takes 50 samples and returns their average value.',
    'responses': {
        '200': {
            'description': 'Average voltage measurement successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'average_voltage': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
        }
    }
})
def get_average_voltage():
    if p is not None:
        v = p.get_average_voltage(samples=50)  # Default to 50 samples
        return jsonify({'status': 'success', 'average_voltage': v})
    return jsonify({'status': 'error', 'message': 'Device not connected'})



@bly.route('/select_range/<string:channel_name>/<int:voltage_range>', methods=['GET'])
@bly.route('/select_range/<string:channel_name>/<float:voltage_range>', methods=['GET'])
@swag_from({
    'tags': ['Measurement'],
    'summary': 'Select voltage measurement range for a channel.',
    'parameters': [
        {
            'name': 'channel_name',
            'in': 'path',
            'required': True,
            'description': 'The name of the channel to configure.',
            'schema': {'type': 'string'}
        },
        {
            'name': 'voltage_range',
            'in': 'path',
            'required': True,
            'description': 'The voltage range to set for measurements.',
            'schema': {'type': 'number', 'format': 'float'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Range set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def select_range(channel_name, voltage_range):
    if p is not None:
        p.select_range(channel_name, voltage_range)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})


@bly.route('/scope_trigger/<string:channel>/<string:name>/<int:voltage>', methods=['GET'])
@bly.route('/scope_trigger/<string:channel>/<string:name>/<float:voltage>', methods=['GET'])
@swag_from({
    'tags': ['Oscilloscope'],
    'summary': 'Configure oscilloscope trigger settings.',
    'operationId': 'scopeTrigger',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'Channel number for trigger (-1 to disable trigger)',
            'schema': {'type': 'string'}
        },
        {
            'name': 'name',
            'in': 'path',
            'required': True,
            'description': 'Trigger type/name',
            'schema': {'type': 'string'}
        },
        {
            'name': 'voltage',
            'in': 'path',
            'required': True,
            'description': 'Trigger voltage level',
            'schema': {'type': 'number', 'format': 'float'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Trigger configured successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
        }
    }
})
def scope_trigger(channel, name, voltage):
    global trigger
    channel = int(channel)
    if channel==-1:
        trigger = False
        return jsonify({'status': 'success'})
    else:
        trigger = True
    if p is not None:
        p.configure_trigger(channel, name, voltage, resolution=10, prescaler=5)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})


@bly.route('/capture1/<string:channel>/<int:ns>/<int:tg>', methods=['GET'])
@swag_from({
    'tags': ['Oscilloscope'],
    'summary': 'Capture data from a single oscilloscope channel.',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The channel to capture (e.g., "A1" , "A2", "A3", "MIC", "SEN").',
            'schema': {'type': 'string'}
        },
        {
            'name': 'ns',
            'in': 'path',
            'required': True,
            'description': 'Number of samples to capture.',
            'schema': {'type': 'integer'}
        },
        {
            'name': 'tg',
            'in': 'path',
            'required': True,
            'description': 'Time gap between samples (microseconds).',
            'schema': {'type': 'integer'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Data capture successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'CH1': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number', 'format': 'float'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number', 'format': 'float'}}
                                }
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
             'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
       }
    }
})
def capture1(channel, ns, tg):
    if p is not None:
        x, y = p.capture1(channel, ns, tg, trigger=trigger)  # Single channel oscilloscope
        return jsonify({'status': 'success', 'CH1': {'timestamps': np.array(x).tolist(), 'voltages': np.array(y).tolist()}})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/capture2/<string:channel>/<int:ns>/<int:tg>', methods=['GET'])
@swag_from({
    'tags': ['Oscilloscope'],
    'summary': 'Capture data from two oscilloscope channels simultaneously.',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The primary channel to capture (e.g., "A1", "A2").',
            'schema': {'type': 'string'}
        },
        {
            'name': 'ns',
            'in': 'path',
            'required': True,
            'description': 'Number of samples to capture.',
            'schema': {'type': 'integer'}
        },
        {
            'name': 'tg',
            'in': 'path',
            'required': True,
            'description': 'Time gap between samples (microseconds).',
            'schema': {'type': 'integer'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Data capture successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'CH1': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number'}}
                                }
                            },
                            'CH2': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number'}}
                                }
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def capture2(channel, ns, tg):
    if p is not None:
        t1, v1, t2, v2 = p.capture2(ns, tg, TraceOneRemap=channel, trigger=trigger)  # Two channel oscilloscope
        return jsonify({'status': 'success', 'CH1': {'timestamps': np.array(t1).tolist(), 'voltages': np.array(v1).tolist()}, 
                                             'CH2': {'timestamps': np.array(t2).tolist(), 'voltages': np.array(v2).tolist()}})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/capture4/<string:channel>/<int:ns>/<int:tg>', methods=['GET'])
@swag_from({
    'tags': ['Oscilloscope'],
    'summary': 'Capture data from four oscilloscope channels simultaneously.',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The primary channel to capture.',
            'schema': {'type': 'string'}
        },
        {
            'name': 'ns',
            'in': 'path',
            'required': True,
            'description': 'Number of samples to capture.',
            'schema': {'type': 'integer'}
        },
        {
            'name': 'tg',
            'in': 'path',
            'required': True,
            'description': 'Time gap between samples (microseconds).',
            'schema': {'type': 'integer'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Data capture successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'CH1': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number'}}
                                }
                            },
                            'CH2': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number'}}
                                }
                            },
                            'CH3': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number'}}
                                }
                            },
                            'CH4': {
                                'type': 'object',
                                'properties': {
                                    'timestamps': {'type': 'array', 'items': {'type': 'number'}},
                                    'voltages': {'type': 'array', 'items': {'type': 'number'}}
                                }
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def capture4(channel, ns, tg):
    if p is not None:
        t1, v1, t2, v2, t3, v3, t4, v4 = p.capture4(ns, tg, TraceOneRemap=channel)  # Four channel oscilloscope
        return jsonify({'status': 'success', 'CH1': {'timestamps': np.array(t1).tolist(), 'voltages': np.array(v1).tolist()}, 
                                             'CH2': {'timestamps': np.array(t2).tolist(), 'voltages': np.array(v2).tolist()},
                                             'CH3': {'timestamps': np.array(t3).tolist(), 'voltages': np.array(v3).tolist()},
                                             'CH4': {'timestamps': np.array(t4).tolist(), 'voltages': np.array(v4).tolist()}
                                             })
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/capture_data/<string:channel>', methods=['GET'])
def capture_data(channel):
    if p is not None:
        #TODO
        pass
        #t1, v1, t2, v2, t3, v3, t4, v4 = p.capture4(ns, tg, TraceOneRemap=channel)  # Four channel oscilloscope
        #return jsonify({'status': 'success', 'CH1': {'timestamps': t1, 'voltages': v1}, 'CH2': {'timestamps': t2, 'voltages': v2}, 'CH3': {'timestamps': t3, 'voltages': v3}, 'CH4': {'timestamps': t4, 'voltages': v4}})
    return jsonify({'status': 'error', 'message': 'Device not connected'})


@bly.route('/set_sine/<int:frequency>', methods=['GET'])
@bly.route('/set_sine/<float:frequency>', methods=['GET'])
@swag_from({
    'tags': ['Wave Generator'],
    'summary': 'Set sine wave frequency.',
    'parameters': [
        {
            'name': 'frequency',
            'in': 'path',
            'required': True,
            'description': 'The frequency of the sine wave in Hz.',
            'schema': {'type': 'number', 'format': 'float'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Sine wave frequency set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def set_sine(frequency):
    if p is not None:
        p.set_sine(frequency)  # Set sine wave frequency
        return jsonify({'status': 'success', 'message': f'Sine wave set to {frequency} Hz'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_wave/<float:frequency>/<string:type>', methods=['GET'])
@bly.route('/set_wave/<int:frequency>/<string:type>', methods=['GET'])
@swag_from({
    'tags': ['Wave Generator'],
    'summary': 'Set waveform type and frequency.',
    'operationId': 'setWave',
    'parameters': [
        {
            'name': 'frequency',
            'in': 'path',
            'required': True,
            'description': 'Frequency of the waveform in Hz',
            'schema': {'type': 'number', 'format': 'float'}
        },
        {
            'name': 'type',
            'in': 'path',
            'required': True,
            'description': 'Type of waveform (e.g., "sine", "square")',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Waveform set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string', 'example': 'Device not connected'}
                        }
                    }
                }
            }
        }
    }
})
def set_wave(frequency, type):
    if p is not None:
        p.set_wave(frequency, type)  # Set frequency and type of waveform
        return jsonify({'status': 'success', 'message': f'Waveform set to {type} at {frequency} Hz'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_sine_amp/<int:value>', methods=['GET'])
@swag_from({
    'tags': ['Wave Generator'],
    'summary': 'Set sine wave amplitude.',
    'parameters': [
        {
            'name': 'value',
            'in': 'path',
            'required': True,
            'description': 'The amplitude value to set.',
            'schema': {'type': 'integer'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Sine wave amplitude set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def set_sine_amp(value):
    if p is not None:
        p.set_sine_amp(value)  # Set sine wave amplitude
        return jsonify({'status': 'success', 'message': f'Sine wave amplitude set to {value}'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/load_equation', methods=['GET'])
@swag_from({
    'tags': ['Wave Generator'],
    'summary': 'Load an arbitrary waveform equation.',
    'description': 'Load an arbitrary shape to the wave generator using a mathematical equation.',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'function': {
                            'type': 'string',
                            'description': 'Mathematical equation defining the waveform'
                        }
                    },
                    'required': ['function']
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Equation loaded successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected or invalid equation.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def load_equation():
    function = request.json.get('function')
    if p is not None and function:
        p.load_equation(function)  # Load an arbitrary shape to WG using an equation
        return jsonify({'status': 'success', 'message': f'Loaded equation: {function}'})
    return jsonify({'status': 'error', 'message': 'Device not connected or function not provided'})

@bly.route('/set_sq1/<int:frequency>/<int:duty_cycle>', methods=['GET'])
@bly.route('/set_sq1/<float:frequency>/<int:duty_cycle>', methods=['GET'])
@swag_from({
    'tags': ['Wave Generator'],
    'summary': 'Set square wave frequency and duty cycle for SQ1.',
    'parameters': [
        {
            'name': 'frequency',
            'in': 'path',
            'required': True,
            'description': 'The frequency of the square wave in Hz.',
            'schema': {'type': 'number', 'format': 'float'}
        },
        {
            'name': 'duty_cycle',
            'in': 'path',
            'required': True,
            'description': 'The duty cycle percentage (0-100).',
            'schema': {'type': 'integer', 'minimum': 0, 'maximum': 100, 'default': 50}
        }
    ],
    'responses': {
        '200': {
            'description': 'Square wave parameters set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def set_sq1(frequency, duty_cycle=50):
    if p is not None:
        p.set_sq1(frequency, duty_cycle)  # Set square wave frequency for SQ1
        return jsonify({'status': 'success', 'message': f'Square wave SQ1 set to {frequency} Hz with {duty_cycle}% duty cycle'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_sq2/<float:frequency>/<int:duty_cycle>', methods=['GET'])
@swag_from({
    'tags': ['Wave Generator'],
    'summary': 'Set square wave frequency and duty cycle for SQ2.',
    'parameters': [
        {
            'name': 'frequency',
            'in': 'path',
            'required': True,
            'description': 'The frequency of the square wave in Hz.',
            'schema': {'type': 'number', 'format': 'float'}
        },
        {
            'name': 'duty_cycle',
            'in': 'path',
            'required': True,
            'description': 'The duty cycle percentage (0-100).',
            'schema': {'type': 'integer', 'minimum': 0, 'maximum': 100, 'default': 50}
        }
    ],
    'responses': {
        '200': {
            'description': 'Square wave parameters set successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def set_sq2(frequency, duty_cycle=50):
    if p is not None:
        p.set_sq2(frequency, duty_cycle)  # Set square wave frequency for SQ2
        return jsonify({'status': 'success', 'message': f'Square wave SQ2 set to {frequency} Hz with {duty_cycle}% duty cycle'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})


@bly.route('/get_resistance', methods=['GET'])
@swag_from({
    'tags': ['Measurements'],
    'summary': 'Measure resistance between SEN and GND.',
    'description': 'Returns the measured resistance value in ohms.',
    'responses': {
        '200': {
            'description': 'Resistance measurement successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'resistance': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_resistance():
    if p is not None:
        resistance = p.get_resistance()  # Measure resistance between SEN and GND
        return jsonify({'status': 'success', 'resistance': resistance})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_capacitance', methods=['GET'])
@swag_from({
    'tags': ['Measurements'],
    'summary': 'Measure capacitance between IN1 and GND.',
    'description': 'Returns the measured capacitance value in farads.',
    'responses': {
        '200': {
            'description': 'Capacitance measurement successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'capacitance': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_capacitance():
    if p is not None:
        capacitance = p.get_capacitance()  # Measure capacitance between IN1 and GND
        return jsonify({'status': 'success', 'capacitance': capacitance})
    return jsonify({'status': 'error', 'message': 'Device not connected'})



@bly.route('/set_state', methods=['GET'])
def set_state():
    data = request.json
    if p is not None:
        p.set_state(SQR1=data.get('SQR1', False), OD1=data.get('OD1', False))  # Set digital states
        return jsonify({'status': 'success', 'message': 'Digital states set successfully'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_states', methods=['GET'])
@swag_from({
    'tags': ['Digital I/O'],
    'summary': 'Get logic levels on all digital input pins.',
    'description': 'Returns the state of all digital input pins.',
    'responses': {
        '200': {
            'description': 'Digital states retrieved successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'states': {
                                'type': 'object',
                                'additionalProperties': {'type': 'boolean'}
                            }
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_states():
    if p is not None:
        states = p.get_states()  # Get logic levels on digital input pins
        return jsonify({'status': 'success', 'states': states})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_state/<string:channel>', methods=['GET'])
@swag_from({
    'tags': ['Digital I/O'],
    'summary': 'Get logic level of a specific digital input pin.',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The digital input channel to read.',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Digital state retrieved successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'channel': {'type': 'string'},
                            'state': {'type': 'boolean'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_state(channel):
    if p is not None:
        state = p.get_state(channel)  # Get logic level on specified digital input pin
        return jsonify({'status': 'success', 'channel': channel, 'state': state})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_freq/<string:channel>', methods=['GET'])
@swag_from({
    'tags': ['Measurements'],
    'summary': 'Measure frequency on specified input channel.',
    'parameters': [
        {
            'name': 'channel',
            'in': 'path',
            'required': True,
            'description': 'The channel to measure frequency from.',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Frequency measurement successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'success'},
                            'channel': {'type': 'string'},
                            'frequency': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Device not connected.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'error'},
                            'message': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_freq(channel):
    if p is not None:
        frequency = p.get_freq(channel)  # Measure frequency on specified input channel
        return jsonify({'status': 'success', 'channel': channel, 'frequency': frequency})
    return jsonify({'status': 'error', 'message': 'Device not connected'})




@bly.route('/get_sensor/<string:sensor>/<string:param>', methods=['GET'])
@swag_from({
    'tags': ['Sensors'],
    'summary': 'Get a specific parameter reading from a sensor.',
    'parameters': [
        {
            'name': 'sensor',
            'in': 'path',
            'required': True,
            'description': 'The sensor identifier.',
            'schema': {'type': 'string'}
        },
        {
            'name': 'param',
            'in': 'path',
            'required': True,
            'description': 'The parameter to read from the sensor.',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Sensor reading successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'value': {'type': 'number', 'format': 'float'}
                        }
                    }
                }
            }
        }
    }
})
def get_sensor(sensor, param):
    result = p.get_sensor(sensor, int(param))
    return jsonify({'value': result})


@bly.route('/get_all_sensors', methods=['GET'])
@swag_from({
    'tags': ['Sensors'],
    'summary': 'Get list of all configured sensors.',
    'description': 'Returns a list of all sensors in the address map with their addresses.',
    'responses': {
        '200': {
            'description': 'Sensor list retrieved successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'sensors': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'List of sensors in format [address]SensorName'
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_all_sensors():
    sensors = []
    if p is not None:
        for addr in p.addressmap:
            sensors.append(f'[{addr}]{p.addressmap[addr]}')
    print('getAllSensors', p.addressmap, sensors)
    return jsonify({'sensors': sensors})

@bly.route('/scan_i2c', methods=['GET'])
@swag_from({
    'tags': ['Sensors'],
    'summary': 'Scan for I2C devices and identify possible sensors.',
    'description': 'Scans the I2C bus and returns a list of detected sensors with their addresses.',
    'responses': {
        '200': {
            'description': 'I2C scan completed successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'sensors': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'List of detected sensors in format [address]SensorName'
                            }
                        }
                    }
                }
            }
        }
    }
})
def scan_i2c():
    global p
    sensors = []
    p.active_sensors = {}  # Empty sensors list
    x = p.I2CScan()
    print('Responses from:', x)
    for a in x:
        possiblesensors = p.sensormap.get(a, [])
        for sens in possiblesensors:
            s = p.namedsensors.get(sens)
            sensors.append(f'[{a}]{s["name"].split(" ")[0]}')
    print('found', sensors)
    return jsonify({'sensors': sensors})


@bly.route('/get_sensor_parameters/<string:name>', methods=['GET'])
@swag_from({
    'tags': ['Sensors'],
    'summary': 'Get parameters available for a specific sensor.',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'required': True,
            'description': 'The name of the sensor.',
            'schema': {'type': 'string'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Sensor parameters retrieved successfully.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'List of available measurement parameters'
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_sensor_parameters(name):
    print('found sensor params for', name, p.namedsensors)
    if name in p.namedsensors:
        return jsonify({'fields': p.namedsensors[name]["fields"]})
    else:
        return jsonify({'fields': ['0']})


@bly.route('/get_generic_sensor/<string:name>/<int:addr>', methods=['GET'])
@swag_from({
    'tags': ['Sensors'],
    'summary': 'Read values from a specific sensor.',
    'parameters': [
        {
            'name': 'name',
            'in': 'path',
            'required': True,
            'description': 'The name of the sensor.',
            'schema': {'type': 'string'}
        },
        {
            'name': 'addr',
            'in': 'path',
            'required': True,
            'description': 'The I2C address of the sensor.',
            'schema': {'type': 'integer'}
        }
    ],
    'responses': {
        '200': {
            'description': 'Sensor reading successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'data': {
                                'type': 'array',
                                'items': {'type': 'number'},
                                'description': 'Array of sensor readings'
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_generic_sensor(name, addr):
    if name not in p.active_sensors:
        p.active_sensors[name] = p.namedsensors[name]
        p.namedsensors[name]['init'](address=addr)
    vals = p.active_sensors[name]['read']()
    #print(vals, type(vals))
    if vals is not None:
        return jsonify({'data': [float(a) for a in vals]})
    else:
        return jsonify({'data': None})
