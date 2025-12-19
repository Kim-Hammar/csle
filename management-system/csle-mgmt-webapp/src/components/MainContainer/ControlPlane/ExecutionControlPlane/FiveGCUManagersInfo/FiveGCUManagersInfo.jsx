import './FiveGCUManagersInfo.css'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import Collapse from 'react-bootstrap/Collapse'
import SpinnerOrButton from '../SpinnerOrButton/SpinnerOrButton.jsx'
import LogsButton from '../LogsButton/LogsButton.jsx'
import {
  FIVE_G_CU_MANAGER_SUBRESOURCE,
  FIVE_G_CU_SUBRESOURCE,
  START_ALL_PROPERTY,
  STOP_ALL_PROPERTY, CU_MONITOR_SUBRESOURCE
} from '../../../../Common/constants'

/**
 * Subcomponent of the /control-plane page that contains information about 5G CU managers
 */
const FiveGCUManagersInfo = (props) => {
  return (
    <Card className="subCard">
      <Card.Header>
        <Button
          onClick={() => props.setFiveGCUManagersOpen(!props.fiveGCUManagersOpen)}
          aria-controls="fiveGCUManagersBody"
          aria-expanded={props.fiveGCUManagersOpen}
          variant="link"
        >
          <h5 className="semiTitle"> 5G CU managers
            <i className="fa fa-server headerIcon" aria-hidden="true"></i>
          </h5>
        </Button>
      </Card.Header>
      <Collapse in={props.fiveGCUManagersOpen}>
        <div id="fiveGCUManagersOpen" className="cardBodyHidden">
          <div className="aggregateActionsContainer">
            <span className="aggregateActions">Stop all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_CU_MANAGER_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={FIVE_G_CU_MANAGER_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all managers:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_CU_MANAGER_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={FIVE_G_CU_MANAGER_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />

            <span className="aggregateActions">Stop all monitors:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${CU_MONITOR_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={CU_MONITOR_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all monitors:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${CU_MONITOR_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={CU_MONITOR_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />

            <span className="aggregateActions">Stop all CUs:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_CU_SUBRESOURCE}-${STOP_ALL_PROPERTY}`)}
              running={true} entity={FIVE_G_CU_SUBRESOURCE}
              name={STOP_ALL_PROPERTY} ip={STOP_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />
            <span className="aggregateActions">Start all CUs:</span>
            <SpinnerOrButton
              loading={props.loadingEntities.includes(
                `${FIVE_G_CU_SUBRESOURCE}-${START_ALL_PROPERTY}`)}
              running={false} entity={FIVE_G_CU_SUBRESOURCE}
              name={START_ALL_PROPERTY} ip={START_ALL_PROPERTY}
              startOrStop={props.startOrStop}
            />

          </div>

          <div className="table-responsive">
            <Table striped bordered hover>
              <thead>
              <tr>
                <th>Service</th>
                <th>IP</th>
                <th>Port</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
              </thead>
              <tbody>
              {props.fiveGCUManagersInfo.five_g_cu_managers_statuses.map((status, index) =>
                <tr key={`${FIVE_G_CU_MANAGER_SUBRESOURCE}-${index}`}>
                  <td>5G CU manager</td>
                  <td>{props.fiveGCUManagersInfo.ips[index]}</td>
                  <td>{props.fiveGCUManagersInfo.ports[index]}</td>
                  {props.activeStatus(props.fiveGCUManagersInfo.five_g_cu_managers_running[index])}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_CU_MANAGER_SUBRESOURCE}-`
                        + `${props.fiveGCUManagersInfo.ips[index]}`)}
                      running={props.fiveGCUManagersInfo.five_g_cu_managers_running[index]}
                      entity={FIVE_G_CU_MANAGER_SUBRESOURCE} name={FIVE_G_CU_MANAGER_SUBRESOURCE}
                      ip={props.fiveGCUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGCUManagersInfo.ips[index]}
                                entity={FIVE_G_CU_MANAGER_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              {props.fiveGCUManagersInfo.five_g_cu_managers_statuses.map((status, index) =>
                <tr key={`${FIVE_G_CU_SUBRESOURCE}-${index}`}>
                  <td>5G CU</td>
                  <td>{props.fiveGCUManagersInfo.ips[index]}</td>
                  <td></td>
                  {props.activeStatus(status.cu_running)}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${FIVE_G_CU_SUBRESOURCE}-`
                        + `${props.fiveGCUManagersInfo.ips[index]}`)}
                      running={status.cu_running}
                      entity={FIVE_G_CU_SUBRESOURCE}
                      name={FIVE_G_CU_SUBRESOURCE}
                      ip={props.fiveGCUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGCUManagersInfo.ips[index]}
                                entity={FIVE_G_CU_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              {props.fiveGCUManagersInfo.five_g_cu_managers_statuses.map((status, index) =>
                <tr key={`${CU_MONITOR_SUBRESOURCE}-${index}`}>
                  <td>CU monitor thread</td>
                  <td>{props.fiveGCUManagersInfo.ips[index]}</td>
                  <td></td>
                  {props.activeStatus(status.monitor_running)}
                  <td>
                    <SpinnerOrButton
                      loading={props.loadingEntities.includes(
                        `${CU_MONITOR_SUBRESOURCE}-`
                        + `${props.fiveGCUManagersInfo.ips[index]}`)}
                      running={status.monitor_running}
                      entity={CU_MONITOR_SUBRESOURCE}
                      name={CU_MONITOR_SUBRESOURCE}
                      ip={props.fiveGCUManagersInfo.ips[index]}
                      startOrStop={props.startOrStop}
                    />
                    <LogsButton name={props.fiveGCUManagersInfo.ips[index]}
                                entity={CU_MONITOR_SUBRESOURCE}
                                getLogs={props.getLogs}
                    />
                  </td>
                </tr>
              )}

              </tbody>
            </Table>
          </div>
        </div>
      </Collapse>
    </Card>
  )

}

FiveGCUManagersInfo.propTypes = {}
FiveGCUManagersInfo.defaultProps = {}
export default FiveGCUManagersInfo
