import { Handle, Position } from 'reactflow';
import PropTypes from 'prop-types';
import './IDS.css';
import ids from './ids-0.png';

/**
 * Component representing an IDS in the network animation in the policy examination page
 */
const IDS = ({ data }) => {
  return (
    <div className="ids">
      <p className="idsLabel largeFont">{data.text}</p>

      <Handle
        type="target"
        position={Position.Top}
        style={{ borderRadius: 0 }}
      />
      <img
        src={ids}
        className="ibm_tower"
        alt="ids"
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

IDS.propTypes = {
  data: PropTypes.shape({
    text: PropTypes.string
  }).isRequired
};

IDS.defaultProps = {};
export default IDS;