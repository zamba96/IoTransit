package model;

import java.util.Collection;
import java.util.Hashtable;

public class LiveTable {


	private Hashtable<Long, Sensor> tabla;

	//private Hashtable<Long, Integer> qTabla;

	/**
	 * numero de sensores
	 */
	private int n;


	/**
	 * Construye una LiveTable para n sensores
	 * @param n el numero de sensores que tiene el sistem
	 */
	public LiveTable(int n) {
		this.n = n;
		tabla = new Hashtable<Long, Sensor>(n);

	}


	public boolean agregarSensor(Sensor s) {
		if(tabla.get(s.getId()) != null)
			return false;

		tabla.put(s.getId(), s);
		return true;
	}
	

	public void actualizarReading(Reading r) throws Exception {
		Sensor s = tabla.get(r.getSensorId());
		if(s == null)
			throw new Exception("No existe el sensor con el Id: " + r.getSensorId());
		s.setLastReadings(r);
	}




}







