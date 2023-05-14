function Sektor(selector, options) {
  this.element = selector;

  const defaultOptions = {
    size: 100,
    stroke: 10,
    arc: false,
    angle: 0,
    sectorColor: '#789',
    circleColor: 'transparent',
    fillCircle: true
  };

  // Merge options with default ones
  options = Object.assign(defaultOptions, options);

  // Reset stroke to 0 if drawing full sector
  options.stroke = options.arc ? options.stroke : 0;

  // Circle dimenstions
  options.center = options.size / 2;
  options.radius = options.stroke ? options.center - (options.stroke) / 2 : options.center;

  this.options = options;

  this.checkAngle();

  const svg =
    `<svg class='Sektor' viewBox='0 0 ${options.size} ${options.size}'>
      <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:rgb(255,162,72);stop-opacity:1" />
          <stop offset="100%" style="stop-color:rgb(255,162,72);stop-opacity:0" />
        </linearGradient>
      </defs>
      ${this.getCircle()}
      ${this.getSector()}
    </svg>`

  this.element.innerHTML = svg;
  this.sector =  this.element.querySelector('.Sektor-sector');
}

Sektor.prototype.checkAngle = function() {
  if (this.options.angle > 360) {
    this.options.angle =  this.options.angle % 360;
  }
};

Sektor.prototype.changeAngle = function(angle) {
  this.options.angle = angle;
  this.checkAngle();
  this.sector.setAttribute('d', this.getSector(true));
};

Sektor.prototype.step = function(angleOffset, endAngle, time, endTime) {
  const now = new Date().valueOf();
  const timeOffset = endTime - now;

  if (timeOffset <= 0) {
    this.changeAngle(endAngle);
  } else {
    const angle = endAngle - (angleOffset * timeOffset / time);

    this.changeAngle(angle);
    requestAnimationFrame(() => this.step(angleOffset, endAngle, time, endTime));
  }
};

Sektor.prototype.animateTo = function(angle, time = 300) {
  if (angle > 360) {
    angle = angle % 360;
  }

  const startTime = new Date().valueOf();
  const endTime = startTime + time;
  const angleOffset = angle - this.options.angle;

  requestAnimationFrame(() => this.step(angleOffset, angle, time, endTime));
};

Sektor.prototype.getSector = function(returnD = false) {
  const options = this.options;

  // Colors
  // const sectorFill = options.arc ? 'none' : options.sectorColor;
  const sectorStroke = options.arc ? options.sectorColor : 'none';

  // Arc angles
  const firstAngle = options.angle > 180 ? 90 : options.angle - 90;
  const secondAngle = -270 + options.angle - 180;

  // Arcs
  const firstArc = this.getArc(firstAngle, options);
  const secondArc = options.angle > 180 ? this.getArc(secondAngle, options) : '';

  // start -> starting line
  // end -> will path be closed or not
  let end = '';
  let start = null;

  if (options.arc) {
    start = `M${options.center},${options.stroke / 2}`;
  } else {
    start = `M${options.center},${options.center} L${options.center},${options.stroke / 2}`;
    end = 'z';
  }

  const d = `${start} ${firstArc} ${secondArc} ${end}`;

  if (returnD) {
    return d;
  }

  return `<path
    class='Sektor-sector'
    stroke-width='${options.stroke}'
    fill='url(#grad1)'
    stroke=${sectorStroke}
    d='${d}' />`;
};

Sektor.prototype.getCircle = function() {
  const options = this.options;
  const circleFill = options.fillCircle || !options.arc ? options.circleColor : 'none';

  return `<circle
      class='Sektor-circle'
      stroke-width='${options.stroke}'
      fill=${circleFill}
      stroke=${options.circleColor}
      cx='${options.center}'
      cy='${options.center}'
      r='${options.radius}' />`;
};

// Generates SVG arc string
Sektor.prototype.getArc = function(angle) {
  const options = this.options;

  const x = options.center + options.radius * Math.cos(this.radians(angle));
  const y = options.center + options.radius * Math.sin(this.radians(angle));

  return `A${options.radius},${options.radius} 1 0 1 ${x},${y}`
};

// Converts from degrees to radians.
Sektor.prototype.radians = function(degrees) {
  return degrees / 180 * Math.PI;
};

export default Sektor