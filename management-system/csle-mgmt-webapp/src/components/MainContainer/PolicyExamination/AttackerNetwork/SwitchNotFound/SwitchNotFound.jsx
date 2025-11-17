import { Handle, Position } from 'reactflow';
import './SwitchNotFound.css';
import gb_switch from './gb_switch.png';

/**
 * Component representing a switch that has not been found by the attacker
 * in the network animation in the policy examination page
 */
const SwitchNotFound = () => {
  return (
    <div className="switchNotFound">
      <Handle
        type="target"
        position={Position.Top}
        style={{ borderRadius: 0 }}
      />
      <img
        src={gb_switch}
        className="ibm_tower"
        alt="gb_switch"
        width="100%"
        height="100%"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ borderRadius: 0 }}
      />
    </div>
  );
};

SwitchNotFound.propTypes = {};
SwitchNotFound.defaultProps = {};
export default SwitchNotFound;