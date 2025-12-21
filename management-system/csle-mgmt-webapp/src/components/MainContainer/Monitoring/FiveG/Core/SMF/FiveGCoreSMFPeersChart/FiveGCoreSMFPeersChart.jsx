import React from 'react'
import './FiveGCoreSMFPeersChart.css'
import {
  CartesianGrid,
  Label,
  Legend, Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'


/**
 * Component containing a plot showing the peers statistics over time for the SMF service in the 5G Core
 */
const FiveGCoreSMFPeersChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats.length > 0) {
      const data = props.stats.map((smf_metrics, index) => {
        return {
          't': (index + 1),
          'Active PFCP peers': parseInt(smf_metrics.pfcp_peers_active),
          'Active GTP peers': parseInt(smf_metrics.gtp_peers_active),
          'Active UEs': parseInt(smf_metrics.ues_active),
          'Active GTPv1 PDP Contexts': parseInt(smf_metrics.gtp1_pdpctxs_active)
        }
      })
      var domain = [0, Math.max(1, data.length)]
      return (
        <div style={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={margin}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="t" type="number" domain={domain}>
                <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont" />
              </XAxis>
              <YAxis type="number">
                <Label angle={270} value="Number of events" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Active PFCP peers"
                    stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                    animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)} />
              <Line animation={props.animation} type="monotone" dataKey="Active GTP peers"
                    stroke="#F08080" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation} />
              <Line animation={props.animation} type="monotone" dataKey="Active UEs"
                    stroke="#8b0000" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation}/>
              <Line animation={props.animation} type="monotone" dataKey="Active GTPv1 PDP Contexts"
                    stroke="#82ca9d" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation}/>
            </LineChart>
          </ResponsiveContainer>
        </div>
      )

    } else {
      return (
        <div></div>
      )
    }
  }
)
FiveGCoreSMFPeersChart.displayName = 'FiveGCoreSMFPeersChart'
FiveGCoreSMFPeersChart.propTypes = {}
FiveGCoreSMFPeersChart.defaultProps = {}
export default FiveGCoreSMFPeersChart
