import { createChart, ColorType } from 'lightweight-charts';
import React, { useEffect, useRef } from 'react';

export const ChartComponent = props => {
	const {
		data,
		colors: {
			backgroundColor = 'white',
			lineColor = '#2962FF',
			textColor = 'black',
		} = {},
	} = props;
	const chartContainerRef = useRef();
	useEffect(
		() => {
			const handleResize = () => {
				chart.applyOptions({ width: chartContainerRef.current.clientWidth });
			};

			const chart = createChart(chartContainerRef.current, {
				layout: {
					background: { type: ColorType.Solid, color: backgroundColor },
					textColor,
				},
				width: chartContainerRef.current.clientWidth,
				height: 300,
			});
			chart.timeScale().fitContent();

			const lineSeries = chart.addLineSeries({ color: '#2962FF' });
			lineSeries.setData(data);

			window.addEventListener('resize', handleResize);

			return () => {
				window.removeEventListener('resize', handleResize);

				chart.remove();
			};
		},
		[data, backgroundColor, lineColor, textColor]
	);

	return (
		<div
			ref={chartContainerRef}
		/>
	);
};

export const getStaticProps = async () => {
	const rawData = await (await fetch('http://api:5000/data/transactions')).json();
	const data = [];
	rawData.forEach(element => {
		data.push({time: element[0].substring(0, 10), value: element[1]});
	});
	return {
		props: {
			data
		}
	};
}

export default function Home({data}) {
  return (
	<ChartComponent data={data}></ChartComponent>
  );
}
