// SVGO config tuned to preserve SMIL animations and referenced IDs.
// The hero SVGs rely on <animate>/<animateTransform>/<animateMotion>,
// masks, clipPaths and filters — none of these may be stripped or renamed.
export default {
  multipass: true,
  js2svg: { indent: 0, pretty: false },
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          // IDs are referenced by url(#...) in masks/filters/gradients — keep them.
          cleanupIds: false,
          // <defs> ordering and grouping is intentional.
          collapseGroups: false,
          moveElemsAttrsToGroup: false,
          moveGroupAttrsToElems: false,
          // Keep viewBox for responsive scaling in the README.
          removeViewBox: false,
          // keyTimes/values on SMIL animations must not be rounded away.
          cleanupNumericValues: { floatPrecision: 3 },
          convertPathData: { floatPrecision: 3 },
          // <title>/<desc> are the accessibility layer.
          removeTitle: false,
          removeDesc: false,
          // Hidden elements may be animation targets.
          removeHiddenElems: false,
          removeUselessDefs: false,
          // Empty attrs like begin="0s" matter for SMIL timing.
          removeEmptyAttrs: false,
          removeUnknownsAndDefaults: {
            keepAriaAttrs: true,
            keepRoleAttr: true,
          },
        },
      },
    },
  ],
};
