package model;

import java.util.ArrayList;

public class Sensor {

	/**
	 * id del sensor
	 */
	private Long id;
	
	/**
	 * description 
	 */
	private String description;
	
	private Reading lastReading;
	
	public Sensor(Long id) {
		this.id = id;
	}
	
	public long getId() {
		return id;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Reading getLastReading() {
		return lastReading;
	}

	public void setLastReadings(Reading lastReadings) {
		this.lastReading = lastReading;
	}
	
}
