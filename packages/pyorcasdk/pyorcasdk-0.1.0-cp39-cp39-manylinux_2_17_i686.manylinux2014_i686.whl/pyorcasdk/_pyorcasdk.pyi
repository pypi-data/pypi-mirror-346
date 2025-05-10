"""
Python binding for the C++ orcaSDK
"""
from __future__ import annotations
import typing
__all__ = ['Actuator', 'ConstF', 'Damper', 'ForceMode', 'HapticEffect', 'HapticMode', 'Inertia', 'KinematicMode', 'MessagePriority', 'MotorMode', 'OrcaError', 'OrcaResultInt16', 'OrcaResultInt32', 'OrcaResultList', 'OrcaResultMotorMode', 'OrcaResultUInt16', 'Osc0', 'Osc1', 'OscillatorType', 'PositionMode', 'Pulse', 'Sine', 'SleepMode', 'Spring0', 'Spring1', 'Spring2', 'SpringCoupling', 'StreamData', 'both', 'important', 'not_important', 'positive']
class Actuator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, name: str, modbus_server_address: int = 1) -> None:
        ...
    @typing.overload
    def __init__(self, serial_interface: ..., clock: ..., name: str, modbus_server_address: int = 1) -> None:
        ...
    @typing.overload
    def begin_serial_logging(self, log_name: str) -> OrcaError:
        ...
    @typing.overload
    def begin_serial_logging(self, log_name: str, log: ...) -> OrcaError:
        ...
    def clear_errors(self) -> OrcaError:
        ...
    def close_serial_port(self) -> None:
        ...
    def disable_stream(self) -> None:
        ...
    def enable_haptic_effects(self, effects: int) -> OrcaError:
        ...
    def enable_stream(self) -> None:
        ...
    def get_errors(self) -> OrcaResultUInt16:
        ...
    def get_force_mN(self) -> OrcaResultInt32:
        ...
    def get_latched_errors(self) -> OrcaResultUInt16:
        ...
    def get_major_version(self) -> OrcaResultUInt16:
        ...
    def get_mode(self) -> OrcaResultMotorMode:
        ...
    def get_position_um(self) -> OrcaResultInt32:
        ...
    def get_power_W(self) -> OrcaResultUInt16:
        ...
    def get_release_state(self) -> OrcaResultUInt16:
        ...
    def get_revision_number(self) -> OrcaResultUInt16:
        ...
    def get_serial_number(self) -> ...:
        ...
    def get_stream_data(self) -> StreamData:
        ...
    def get_temperature_C(self) -> OrcaResultUInt16:
        ...
    def get_voltage_mV(self) -> OrcaResultUInt16:
        ...
    @typing.overload
    def open_serial_port(self, port_number: int, baud_rate: int = 19200, interframe_delay: int = 2000) -> OrcaError:
        """
        Open serial port using port number
        """
    @typing.overload
    def open_serial_port(self, port_path: str, baud_rate: int = 19200, interframe_delay: int = 2000) -> OrcaError:
        """
        Open serial port using port path
        """
    def read_multiple_registers_blocking(self, reg_start_address: int, num_registers: int, priority: MessagePriority = ...) -> OrcaResultList:
        ...
    def read_register_blocking(self, reg_address: int, priority: MessagePriority = ...) -> OrcaResultUInt16:
        ...
    def read_wide_register_blocking(self, reg_address: int, priority: MessagePriority = ...) -> OrcaResultInt32:
        ...
    def read_write_multiple_registers_blocking(self, read_starting_address: int, read_num_registers: int, write_starting_address: int, write_num_registers: int, write_data: int, priority: MessagePriority = ...) -> OrcaResultList:
        ...
    def run(self) -> None:
        ...
    def set_constant_force(self, force: int) -> OrcaError:
        ...
    def set_constant_force_filter(self, force_filter: int) -> OrcaError:
        ...
    def set_damper(self, damping: int) -> OrcaError:
        ...
    def set_inertia(self, inertia: int) -> OrcaError:
        ...
    def set_kinematic_motion(self, id: int, position: int, time: int, delay: int, type: int, auto_next: int, next_id: int = -1) -> OrcaError:
        ...
    def set_max_force(self, max_force: int) -> OrcaError:
        ...
    def set_max_power(self, set_max_power: int) -> OrcaError:
        ...
    def set_max_temp(self, max_temp: int) -> OrcaError:
        ...
    def set_mode(self, orca_mode: MotorMode) -> OrcaError:
        ...
    def set_osc_effect(self, osc_id: int, amplitude: int, frequency_dhz: int, duty: int, type: OscillatorType) -> OrcaError:
        ...
    def set_pctrl_tune_softstart(self, t_in_ms: int) -> OrcaError:
        ...
    def set_safety_damping(self, max_safety_damping: int) -> OrcaError:
        ...
    def set_spring_effect(self, spring_id: int, gain: int, center: int, dead_zone: int = 0, saturation: int = 0, coupling: SpringCoupling = ...) -> OrcaError:
        ...
    def set_streamed_force_mN(self, force: int) -> None:
        ...
    def set_streamed_position_um(self, position: int) -> None:
        ...
    def time_since_last_response_microseconds(self) -> int:
        ...
    def trigger_kinematic_motion(self, id: int) -> OrcaError:
        ...
    def tune_position_controller(self, pgain: int, igain: int, dvgain: int, sat: int, dgain: int = 0) -> None:
        ...
    def update_haptic_stream_effects(self, effects: int) -> None:
        ...
    def write_multiple_registers_blocking(self, reg_start_address: int, num_registers: int, write_data: int, priority: MessagePriority = ...) -> OrcaError:
        ...
    def write_register_blocking(self, reg_address: int, write_data: int, priority: MessagePriority = ...) -> OrcaError:
        ...
    def write_wide_register_blocking(self, reg_address: int, write_data: int, priority: MessagePriority = ...) -> OrcaError:
        ...
    def zero_position(self) -> OrcaError:
        ...
    @property
    def name(self) -> str:
        ...
class HapticEffect:
    """
    Members:
    
      ConstF
    
      Spring0
    
      Spring1
    
      Spring2
    
      Damper
    
      Inertia
    
      Osc0
    
      Osc1
    """
    ConstF: typing.ClassVar[HapticEffect]  # value = <HapticEffect.ConstF: 1>
    Damper: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Damper: 16>
    Inertia: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Inertia: 32>
    Osc0: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Osc0: 64>
    Osc1: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Osc1: 128>
    Spring0: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Spring0: 2>
    Spring1: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Spring1: 4>
    Spring2: typing.ClassVar[HapticEffect]  # value = <HapticEffect.Spring2: 8>
    __members__: typing.ClassVar[dict[str, HapticEffect]]  # value = {'ConstF': <HapticEffect.ConstF: 1>, 'Spring0': <HapticEffect.Spring0: 2>, 'Spring1': <HapticEffect.Spring1: 4>, 'Spring2': <HapticEffect.Spring2: 8>, 'Damper': <HapticEffect.Damper: 16>, 'Inertia': <HapticEffect.Inertia: 32>, 'Osc0': <HapticEffect.Osc0: 64>, 'Osc1': <HapticEffect.Osc1: 128>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MessagePriority:
    """
    Members:
    
      important
    
      not_important
    """
    __members__: typing.ClassVar[dict[str, MessagePriority]]  # value = {'important': <MessagePriority.important: 0>, 'not_important': <MessagePriority.not_important: 1>}
    important: typing.ClassVar[MessagePriority]  # value = <MessagePriority.important: 0>
    not_important: typing.ClassVar[MessagePriority]  # value = <MessagePriority.not_important: 1>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MotorMode:
    """
    Members:
    
      SleepMode
    
      ForceMode
    
      PositionMode
    
      HapticMode
    
      KinematicMode
    """
    ForceMode: typing.ClassVar[MotorMode]  # value = <MotorMode.ForceMode: 2>
    HapticMode: typing.ClassVar[MotorMode]  # value = <MotorMode.HapticMode: 4>
    KinematicMode: typing.ClassVar[MotorMode]  # value = <MotorMode.KinematicMode: 5>
    PositionMode: typing.ClassVar[MotorMode]  # value = <MotorMode.PositionMode: 3>
    SleepMode: typing.ClassVar[MotorMode]  # value = <MotorMode.SleepMode: 1>
    __members__: typing.ClassVar[dict[str, MotorMode]]  # value = {'SleepMode': <MotorMode.SleepMode: 1>, 'ForceMode': <MotorMode.ForceMode: 2>, 'PositionMode': <MotorMode.PositionMode: 3>, 'HapticMode': <MotorMode.HapticMode: 4>, 'KinematicMode': <MotorMode.KinematicMode: 5>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OrcaError:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __bool__(self) -> bool:
        ...
    def __init__(self, failure_type: int, error_message: str = '') -> None:
        ...
    def __repr__(self) -> str:
        ...
    def what(self) -> str:
        ...
class OrcaResultInt16:
    error: OrcaError
    value: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class OrcaResultInt32:
    error: OrcaError
    value: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class OrcaResultList:
    error: OrcaError
    value: list[int]
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class OrcaResultMotorMode:
    error: OrcaError
    value: MotorMode
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class OrcaResultUInt16:
    error: OrcaError
    value: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
class OscillatorType:
    """
    Members:
    
      Pulse
    
      Sine
    
      Triangle 
    
      Saw  
    """
    Pulse: typing.ClassVar[OscillatorType]  # value = <OscillatorType.Pulse: 0>
    Sine: typing.ClassVar[OscillatorType]  # value = <OscillatorType.Sine: 1>
    __members__: typing.ClassVar[dict[str, OscillatorType]]  # value = {'Pulse': <OscillatorType.Pulse: 0>, 'Sine': <OscillatorType.Sine: 1>, 'Triangle ': <OscillatorType.Triangle : 2>, 'Saw  ': <OscillatorType.Saw  : 3>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SpringCoupling:
    """
    Members:
    
      both
    
      positive
    
      negative 
    """
    __members__: typing.ClassVar[dict[str, SpringCoupling]]  # value = {'both': <SpringCoupling.both: 0>, 'positive': <SpringCoupling.positive: 1>, 'negative ': <SpringCoupling.negative : 2>}
    both: typing.ClassVar[SpringCoupling]  # value = <SpringCoupling.both: 0>
    positive: typing.ClassVar[SpringCoupling]  # value = <SpringCoupling.positive: 1>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class StreamData:
    errors: int
    force: int
    position: int
    power: int
    temperature: int
    voltage: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
ConstF: HapticEffect  # value = <HapticEffect.ConstF: 1>
Damper: HapticEffect  # value = <HapticEffect.Damper: 16>
ForceMode: MotorMode  # value = <MotorMode.ForceMode: 2>
HapticMode: MotorMode  # value = <MotorMode.HapticMode: 4>
Inertia: HapticEffect  # value = <HapticEffect.Inertia: 32>
KinematicMode: MotorMode  # value = <MotorMode.KinematicMode: 5>
Osc0: HapticEffect  # value = <HapticEffect.Osc0: 64>
Osc1: HapticEffect  # value = <HapticEffect.Osc1: 128>
PositionMode: MotorMode  # value = <MotorMode.PositionMode: 3>
Pulse: OscillatorType  # value = <OscillatorType.Pulse: 0>
Sine: OscillatorType  # value = <OscillatorType.Sine: 1>
SleepMode: MotorMode  # value = <MotorMode.SleepMode: 1>
Spring0: HapticEffect  # value = <HapticEffect.Spring0: 2>
Spring1: HapticEffect  # value = <HapticEffect.Spring1: 4>
Spring2: HapticEffect  # value = <HapticEffect.Spring2: 8>
both: SpringCoupling  # value = <SpringCoupling.both: 0>
important: MessagePriority  # value = <MessagePriority.important: 0>
not_important: MessagePriority  # value = <MessagePriority.not_important: 1>
positive: SpringCoupling  # value = <SpringCoupling.positive: 1>
