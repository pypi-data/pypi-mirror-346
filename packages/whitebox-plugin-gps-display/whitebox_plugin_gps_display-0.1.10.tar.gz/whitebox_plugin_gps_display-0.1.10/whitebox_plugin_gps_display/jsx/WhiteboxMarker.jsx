import {useEffect, useRef} from "react";
import {
  Marker,
  useMap,
} from 'react-leaflet';
import useMapStore from "./stores/map";

const WhiteboxMarker = () => {
  const map = useMap();

  const markerRef = useRef(null);
  const markerWhitebox = useMapStore((state) => state.markerWhitebox);

  const defaultFollowZoom = useMapStore((state) => state.defaultFollowZoom);

  const follow = useMapStore((state) => state.follow);
  const setFollow = useMapStore((state) => state.setFollow);

  useEffect(() => {
    if (!markerWhitebox) return;

    // Animate the map
    if (follow) {
      map.flyTo(markerWhitebox);
    }

    // Move the marker without the full re-render
    if (markerRef.current) {
      markerRef.current.setLatLng(markerWhitebox);
    }
  }, [map, markerWhitebox]);

  // If the marker location is not yet initialized, don't render anything
  if (!markerWhitebox) return null;

  return (
    <Marker
      position={markerWhitebox}
      ref={markerRef}
      eventHandlers={{
        click: () => {
          map.setView(markerWhitebox, defaultFollowZoom);
          setFollow(true);
        },
      }}
    />
  );
};

export {
  WhiteboxMarker,
};
export default WhiteboxMarker;