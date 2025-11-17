import { Handle, Position } from 'reactflow';
import PropTypes from 'prop-types';
import './Attacker.css';
import hacker from './hacker.png';

const attackerStyles = {
  background: '#FFFF',
  color: '#000000',
  padding: 0,
};

/**
 * Component representing an attacker in the network animation in the policy examination page
 */
const Attacker = ({ data }) => {
  return (
    <div style={attackerStyles}>
      <div className="largeFont">{data.text}</div>
      <img
        src={hacker}
        className="attacker"
        alt="attacker"
        width="25%"
        height="25%"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ borderRadius: 0 }}
      />
    </div>
  );
};

Attacker.propTypes = {
  data: PropTypes.shape({
    text: PropTypes.string
  }).isRequired
};

Attacker.defaultProps = {};
export default Attacker;