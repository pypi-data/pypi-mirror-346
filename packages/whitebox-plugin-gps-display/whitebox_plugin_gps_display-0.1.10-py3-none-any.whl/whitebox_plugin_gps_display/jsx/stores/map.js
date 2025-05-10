/* This file creates a Zustand store for managing the state of the map,
 * including the marker coordinates and control settings.
 *
 * The `react-leaflet`'s components are utilized using this state store, meaning
 * that the map and its controls are reactive to the state changes in this store.
 */
import {create} from "zustand";

const createMarkerSlice = (set) => ({
  markerWhitebox: null,
  markerFlights: [],

  setWhiteboxCoordinates: (coordinates) => {
    set({
      markerWhitebox: coordinates,
    })
  }
})

const createControlSlice = (set) => ({
  defaultFollowZoom: 12,

  follow: true,

  setFollow: (follow) => set({follow}),
})

const useMapStore = create((...a) => ({
  ...createMarkerSlice(...a),
  ...createControlSlice(...a),
}));

export default useMapStore;
