import { Handle, Position } from 'reactflow';
import './ApplicationServer.css';
import ibm_tower from './ibm_tower_small.png';

/**
 * Component representing an application server in the network animation in the policy examination page
 */
const ApplicationServer = () => {
  return (
    <div className="appServer">
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

ApplicationServer.propTypes = {};
ApplicationServer.defaultProps = {};
export default ApplicationServer;