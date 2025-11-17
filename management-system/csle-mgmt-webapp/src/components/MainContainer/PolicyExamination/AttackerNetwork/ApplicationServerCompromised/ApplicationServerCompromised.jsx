import { Handle, Position } from 'reactflow';
import './ApplicationServerCompromised.css';
import ibm_tower from './ibm_tower_small_compromised.png';

/**
 * Component representing a compromised application server in the network animation in the policy examination page
 */
const ApplicationServerCompromised = () => {
  return (
    <div className="appServerCompromised">
      <Handle
        type="target"
        position={Position.Top}
        style={{ borderRadius: 0 }}
      />
      <img
        src={ibm_tower}
        className="ibm_tower"
        alt="ibm_tower"
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

ApplicationServerCompromised.propTypes = {};
ApplicationServerCompromised.defaultProps = {};
export default ApplicationServerCompromised;