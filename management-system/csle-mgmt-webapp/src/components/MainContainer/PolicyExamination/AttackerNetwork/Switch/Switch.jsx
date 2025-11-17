import { Handle, Position } from 'reactflow';
import './Switch.css';
import gb_switch from './gb_switch.png';

/**
 * Component representing a switch in the network animation in the policy examination page
 */
const Switch = () => {
  return (
    <div className="switch">
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

Switch.propTypes = {};
Switch.defaultProps = {};
export default Switch;